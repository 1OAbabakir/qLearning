from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from io import TextIOWrapper
import csv
from datetime import date
from django.http import HttpResponse
from .utils.image_utils import process_image_from_path

from .forms import LoginForm, CardForm, CsvUploadForm, RegisterForm
from .models import Card

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user)
                return redirect('dashboard')
            messages.error(request, "Login fehlgeschlagen.")
    else:
        form = LoginForm()
    return render(request, "flashcards/login.html", {"form": form})

def register_view(request):
    # Wenn der User schon eingeloggt ist, nicht noch mal registrieren
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # User aus dem Formular speichern
            user = form.save()
            # Optional: direkt einloggen
            login(request, user)
            messages.success(request, "Registrierung erfolgreich. Willkommen!")
            return redirect('dashboard')
        else:
            # Ungültig -> Fehler im Template anzeigen
            messages.error(request, "Bitte korrigiere die markierten Felder.")
    else:
        form = RegisterForm()

    return render(request, "flashcards/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    qs = Card.objects.filter(owner=request.user)
    due = qs.filter(next_due__lte=date.today()).count()
    total = qs.count()
    categories = (
        qs.values("category")
          .order_by("category")
          .annotate(cnt=Count("id"))
    )
    return render(request, "flashcards/dashboard.html", {"due": due, "total": total, "categories": categories})

@login_required
def add_card(request):
    single_form = CardForm()
    csv_form = CsvUploadForm()

    if request.method == "POST":
        # Prüfen, ob CSV-Upload kommt (enctype multipart + file-Feld)
        if request.FILES.get("file"):
            csv_form = CsvUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                uploaded = request.FILES["file"]
                # UTF-8 (mit/ohne BOM) lesen
                wrapper = TextIOWrapper(uploaded.file, encoding="utf-8-sig", newline="")
                # Trennzeichen automatisch erkennen (Komma/Semikolon)
                sample = wrapper.read(2048)
                wrapper.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=",;")
                except csv.Error:
                    dialect = csv.excel
                    dialect.delimiter = ","
                reader = csv.reader(wrapper, dialect)

                created, skipped, bad = 0, 0, 0
                for row in reader:
                    if not row:
                        continue
                    if len(row) < 2:
                        bad += 1
                        continue
                    question = row[0].strip()
                    answer = row[1].strip()
                    category = (row[2].strip() if len(row) >= 3 else "vokabel")
                    if not question or not answer:
                        bad += 1
                        continue
                    # Duplikate vermeiden (pro Owner)
                    exists = Card.objects.filter(owner=request.user, question=question, answer=answer, category=category).exists()
                    if exists:
                        skipped += 1
                        continue
                    Card.objects.create(owner=request.user, question=question, answer=answer, category=category)
                    created += 1

                messages.success(request, f"CSV importiert: {created} neu, {skipped} übersprungen (Duplikate), {bad} fehlerhaft.")
                return redirect('add_card')
            else:
                messages.error(request, "CSV-Upload fehlgeschlagen. Bitte Datei prüfen.")
        else:
            # Einzel-Eingabe
            single_form = CardForm(request.POST, request.FILES)
            if single_form.is_valid():
                card = single_form.save(commit=False)
                card.owner = request.user
                card.save()
                messages.success(request, "Vokabel angelegt.")
                return redirect('add_card')

    return render(request, "flashcards/add_card.html", {
        "form": single_form,
        "csv_form": csv_form
    })

@login_required
def study(request, category):
    # Simple reveal flow: show question, reveal answer, next card
    direction = request.GET.get("dir") or "Frage → Antwort"

    categories = (
        Card.objects
            .filter(owner=request.user)
            .values("category")
            .order_by("category")
            .annotate(cnt=Count("id"))
    )

    card = None
    prompt = "Keine Karten fällig"

    if request.method == "POST":
        # Keep the same card by ID to avoid changing on reveal
        card_id = request.POST.get("card_id")
        if card_id:
            card = Card.objects.filter(owner=request.user, id=card_id, category=category).first()
        if not card:
            card = Card.objects.filter(owner=request.user, category=category, next_due__lte=date.today()).order_by("?").first()
        if card:
            prompt = f"{card.question} → {card.answer}"
    else:
        # GET: pick a random due card in the category
        card = Card.objects.filter(owner=request.user, category=category, next_due__lte=date.today()).order_by("?").first()
        if card:
            prompt = f"{card.question}"

    return render(request, "flashcards/study.html", {
        "card": card,
        "category": category,
        "categories": categories,
        "prompt": prompt,
        "direction": direction,
    })


@login_required
def card_image(request, card_id):
    """Return a processed image for a card. Query params: rotate, w, h, thumb (1)

    Example: /card/5/image/?w=600&rotate=90
    """
    card = get_object_or_404(Card, id=card_id, owner=request.user)
    if not card.image:
        return HttpResponse(status=404)

    try:
        rotate = int(request.GET.get('rotate', 0))
    except ValueError:
        rotate = 0
    try:
        w = int(request.GET.get('w')) if request.GET.get('w') else None
    except ValueError:
        w = None
    try:
        h = int(request.GET.get('h')) if request.GET.get('h') else None
    except ValueError:
        h = None

    thumb = request.GET.get('thumb') == '1'
    fmt = request.GET.get('fmt', 'JPEG')

    data, mime = process_image_from_path(card.image.path, rotate=rotate, width=w, height=h, thumb=thumb, fmt=fmt)
    return HttpResponse(data, content_type=mime)