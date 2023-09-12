from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from htmltopdf.utils import html_to_pdf
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

def pdf_generate_page(request, match_id):
    # Fetch data from your model or context
    match_data = fixture.objects.get(match_id=match_id)
    home_players = team_player.objects.filter(team_id=match_data.team_id)
    away_players = away_team_player.objects.filter(team_id=match_data.away_team_id)
    
    # Create a response object with a PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="match_details.pdf"'

    # Create a PDF document using reportlab (letter-sized layout)
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Define custom styles, including a Bold style
    styles = {
        'Title': ParagraphStyle(
            name='Title',
            fontSize=16,
            leading=18,
            alignment=1,
            fontName='Helvetica-Bold',
        ),
        'Heading2': ParagraphStyle(
            name='Heading2',
            fontSize=14,
            leading=16,
            alignment=0,
            spaceAfter=12,
        ),
        'Heading3': ParagraphStyle(
            name='Heading3',
            fontSize=12,
            leading=14,
            alignment=0,
            spaceAfter=6,
            fontName='Helvetica-Bold',
        ),
        'Bold': ParagraphStyle(
            name='Bold',
            fontSize=12,
            leading=14,
            fontName='Helvetica-Bold',
        ),
        'Normal': ParagraphStyle(
            name='Normal',
            fontSize=12,
            leading=14,
        ),
    }

    # Create a list of flowables (elements) for the PDF content
    story = []

    # Add a title (centered)
    title = Paragraph(match_data.name, styles['Title'])
    story.append(title)
    story.append(Spacer(1, 24))  # Add some space

    # General Details
    story.append(Paragraph('<strong>General Details</strong>', styles['Heading2']))
    
    # Create a table for general details
    general_table_data = [
        [Paragraph('Name:', styles['Bold']), match_data.name],
        [Paragraph('Venue:', styles['Bold']), match_data.venue],
        [Paragraph('Date:', styles['Bold']), match_data.date],
        [Paragraph('Status:', styles['Bold']), match_data.status],
    ]
    general_table = Table(general_table_data, colWidths=[100, 400])
    general_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(general_table)
    story.append(Spacer(1, 12))  # Add some space

    # Create a table for team details (including both home and away teams)
    team_details_data = [
        [Paragraph('<strong>Team Details</strong>', styles['Heading2'])],
        [Paragraph('<strong>Home Team</strong>', styles['Heading3']),
         Paragraph('<strong>Away Team</strong>', styles['Heading3'])],
        # [Paragraph('Team Name:', styles['Bold']),
        #  Paragraph('Team Name:', styles['Bold'])],
    ]

    # Collect home team player names
    home_players_data = []
    for player in home_players:
        home_players_data.append(Paragraph(f'{player.player_id.firstname} {player.player_id.lastname}', styles['Normal']))

    # Collect away team player names
    away_players_data = []
    for player in away_players:
        away_players_data.append(Paragraph(f'{player.player_id.firstname} {player.player_id.lastname}', styles['Normal']))

    # Add home and away team details to the table
    team_details_data.append([Paragraph(match_data.team_id.name, styles['Normal']),
                             Paragraph(match_data.away_team_id.name, styles['Normal'])])
    team_details_data.append([Paragraph('Team Members:', styles['Bold']),
                             Paragraph('Team Members:', styles['Bold'])])
    team_details_data.append([home_players_data, away_players_data])

    # Create the team details table
    team_details_table = Table(team_details_data, colWidths=[250, 250])
    team_details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(team_details_table)

    # Build the PDF document
    doc.build(story)

    return response


context = {
    'data': {
        'name': "Test Name",
        'club': "Real madrid",
    }
}
match = {
    'data': {
        'opponent': "Opponent Team",
        'our_team': "Our Team",
        'date': "2023-09-15",
        'location': "Stadium Name",
    }
}
def match_detail(request):    
    return render(request=request, template_name='match_detail.html', match= match)

def index(request):
    try:
        auth.logout(request)
    except:
        pass
    admin_id = User.objects.get(username='admin')
    our_club = club.objects.get(admin_id=admin_id)
    players = player.objects.filter(club_id=our_club)[:6]
    context = {'players': players}
    return render(request=request, template_name='index.html', context=context)

def documents(request):
    match_data = fixture.objects.all()
    context = {'match_data': match_data}
    return render(request=request, template_name='documents.html', context=context)

def view_clubs(request):
    club_data = away_club.objects.all()
    context = {'club_data': club_data}
    return render(request=request, template_name='clubs.html', context=context)

def matches(request):
    match_data = fixture.objects.all()
    context = {'match_data': match_data}
    return render(request=request, template_name='matches.html', context=context)

def upcoming_matches(request):
    match_data = fixture.objects.all()
    context = {'match_data': match_data, 'ctx': 'Upcoming'}
    return render(request=request, template_name='upcoming_matches.html', context=context)

def upcoming_match_data(request, match_id):
    match_data = fixture.objects.get(match_id=match_id)
    home_players = team_player.objects.filter(team_id=match_data.team_id)
    away_players = away_team_player.objects.filter(team_id=match_data.away_team_id)
    context = {'match_data': match_data, 'home_players': home_players, 'away_players': away_players}
    return render(request=request, template_name='view_upcoming_match_data.html', context=context)

def test(request):
    return render(request=request, template_name='test.html', context=context)

def generate_pdf(request):
    pdf = html_to_pdf('pdf_generate_page.html', context=context)
    return HttpResponse(pdf, content_type='application/pdf')

def about(request):
    admin_data = User.objects.get(username='admin')
    club_data = club.objects.get(admin_id = admin_data)
    context = {'club_data': club_data}
    return render(request, 'about.html', context)


def loginpage(request):
    return render(request=request, template_name='admin/loginpage.html', context=context)

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			request.session['hello'] = username
			messages.info(request, f'Welcome {username}.')
			return redirect(adminindex)
		else:
			messages.info(request, 'Invalid Username or Password. Try Again.')
			return redirect(loginpage)
	else:
		messages.info(request, 'Oops, Something went wrong.')
		return redirect(loginpage)

def logout(request):
	auth.logout(request)
	return redirect(loginpage)

@login_required(login_url=loginpage)
def adminindex(request):
    return render(request=request, template_name='admin/home/adminindex.html', context=context)

@login_required(login_url=loginpage)
def add_player(request):
    return render(request=request, template_name='admin/home/add_player.html', context=context)

@login_required(login_url=loginpage)
def add_player_data(request):
    user = request.user
    club_data = club.objects.get(admin_id=user)
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        matches_played = request.POST['matches_played']
        goals = request.POST['goals']
        try:
            image = request.FILES['image']
        except:
            image = f'media/default.jpg'
        playerdata = player(firstname=firstname, lastname=lastname, matches_played=matches_played, goals=goals, club_id=club_data, image=image)
        playerdata.save()
        return redirect(show_players)

@login_required(login_url=loginpage)
def edit_player_data(request, player_id):
    player_data = player.objects.get(player_id=player_id)
    context = {"player": player_data}
    return render(request, template_name='admin/home/edit_player.html', context=context)

@login_required(login_url=loginpage)
def update_player(request, player_id):
    player_data = player.objects.get(player_id=player_id)
    player_data.firstname = request.POST.get('firstname')
    player_data.lastname = request.POST.get('lastname')
    player_data.matches_played = request.POST.get('matches_played')
    player_data.goals = request.POST.get('goals')
    try:
        player_data.image = request.FILES['image']
    except:
        pass
    player_data.save()
    return redirect(show_players)
    
@login_required(login_url=loginpage) 
def delete_player(request, player_id):
    player_data = player.objects.get(player_id=player_id)
    player_data.delete()
    return redirect(show_players)
    
@login_required(login_url=loginpage)
def show_players(request):
    players = player.objects.all()
    context = {"players": players}
    return render(request=request, template_name='admin/home/show_players.html', context=context)

@login_required(login_url=loginpage)
def add_team(request):
    players_data = player.objects.all()
    context = {"players": players_data}
    return render(request=request, template_name='admin/home/add_team.html', context=context)

@login_required(login_url=loginpage)
def create_team(request):
    if request.method == 'POST':
        user = request.user
        clubdata = club.objects.get(admin_id=user)
        name = request.POST['name']
        teamdata = team(club_id=clubdata, name=name)
        teamdata.save()
        players = [request.POST['player1'], request.POST['player2'], request.POST['player3'], request.POST['player4'], request.POST['player5'], request.POST['player6'], request.POST['player7'], request.POST['player8'], request.POST['player9'], request.POST['player10'], request.POST['player11']]
        for playerdata in players:
            player_data = player.objects.get(player_id=playerdata)
            teamplayer_data = team_player(team_id=teamdata, player_id=player_data)
            teamplayer_data.save()
        return redirect(show_teams)

@login_required(login_url=loginpage)
def show_teams(request):
    teamdata = team.objects.all()
    teamplayer_data = team_player.objects.all()
    players = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    context = {'teams': teamdata, 'teamplayers': teamplayer_data, "players": players}
    return render(request=request, template_name='admin/home/show_team.html', context=context)

@login_required(login_url=loginpage)
def edit_team_data(request, team_id):
    teamplayers = []
    playernumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    team_data = team.objects.get(team_id=team_id)
    players = player.objects.all()
    teamplayer_data = team_player.objects.filter(team_id=team_data)
    for i, j in zip(teamplayer_data, playernumber):
        tp = []
        tp.append(i.player_id.player_id)
        tp.append(i.player_id.firstname)
        tp.append(i.player_id.lastname)
        tp.append(j)
        teamplayers.append(tp)
    context = {"team": team_data, "teamplayers": teamplayers, "players": players}
    return render(request, template_name='admin/home/edit_team_data.html', context=context)

@login_required(login_url=loginpage)
def update_team(request, team_id):
    team_data = team.objects.get(team_id=team_id)
    team_data.name = request.POST.get('name')
    team_data.save()
    players = [request.POST.get('player1'), request.POST.get('player2'), request.POST.get('player3'), request.POST.get('player4'), request.POST.get('player5'), request.POST.get('player6'), request.POST.get('player7'), request.POST.get('player8'), request.POST.get('player9'), request.POST.get('player10'), request.POST.get('player11')]
    teamplayer_data = team_player.objects.filter(team_id=team_data.team_id)
    for td, p in zip(teamplayer_data, players):
        player_data = player.objects.get(player_id=p)
        td.player_id = player_data
        td.save()
    return redirect(show_teams)

@login_required(login_url=loginpage) 
def delete_team(request, team_id):
    team_data = team.objects.get(team_id=team_id)
    team_data.delete()
    return redirect(show_teams)


@login_required(login_url=loginpage)
def add_club(request):
    return render(request=request, template_name='admin/home/add_club.html', context=context)

@login_required(login_url=loginpage)
def show_clubs(request):
    return render(request=request, template_name='admin/home/show_clubs.html', context=context)


@login_required(login_url=loginpage)
def add_away_club(request):
    return render(request, 'admin/away/add_away_club.html')

@login_required(login_url=loginpage)
def add_awayclub_data(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        try:
            image = request.FILES['image']
        except:
            image = f'media/default.jpg'
        awayclub_data = away_club(name=name, email=email, phone=phone, location=location, image=image)
        awayclub_data.save()
        return redirect(show_away_club)
    
    
@login_required(login_url=loginpage)
def show_away_club(request):
    clubs = away_club.objects.all()
    context = {'clubs': clubs}
    return render(request, 'admin/away/show_away_club.html', context)

@login_required(login_url=loginpage)
def edit_away_club(request, club_id):
    club_data = away_club.objects.get(club_id=club_id)
    context = {"club_data": club_data}
    return render(request, template_name='admin/away/edit_away_club.html', context=context)


@login_required(login_url=loginpage)
def update_away_club(request, club_id):
    club_data = away_club.objects.get(club_id=club_id)
    club_data.name = request.POST.get('name')
    club_data.email = request.POST.get('email')
    club_data.phone = request.POST.get('phone')
    club_data.location = request.POST.get('location')
    try:
        club_data.image = request.FILES('image')
    except:
        pass
    club_data.save()
    return redirect(show_away_club)

@login_required(login_url=loginpage) 
def delete_away_club(request, club_id):
    club_data = away_club.objects.get(club_id=club_id)
    club_data.delete()
    return redirect(show_away_club)

@login_required(login_url=loginpage)
def add_away_player(request):
    clubs = away_club.objects.all()
    context = {"clubs": clubs}
    return render(request=request, template_name='admin/away/add_away_player.html', context=context)

@login_required(login_url=loginpage)
def add_awayplayer_data(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        matches_played = request.POST['matches_played']
        goals = request.POST['goals']
        try:
            image = request.FILES['image']
        except:
            image = f'media/default.jpg'
        club_id = request.POST['clubid']
        club_data = away_club.objects.get(club_id=club_id)
        playerdata = away_player(firstname=firstname, lastname=lastname, matches_played=matches_played, goals=goals, club_id=club_data)
        playerdata.save()
        return redirect(show_away_players)

@login_required(login_url=loginpage)
def edit_awayplayer_data(request, player_id):
    player_data = away_player.objects.get(player_id=player_id)
    context = {"player": player_data}
    return render(request, template_name='admin/away/edit_away_player.html', context=context)

@login_required(login_url=loginpage)
def update_awayplayer(request, player_id):
    player_data = away_player.objects.get(player_id=player_id)
    player_data.firstname = request.POST.get('firstname')
    player_data.lastname = request.POST.get('lastname')
    player_data.matches_played = request.POST.get('matches_played')
    player_data.goals = request.POST.get('goals')
    try:
        image = request.FILES['image']
    except:
        pass
    player_data.save()
    return redirect(show_away_players)
    
@login_required(login_url=loginpage) 
def delete_awayplayer(request, player_id):
    player_data = away_player.objects.get(player_id=player_id)
    player_data.delete()
    return redirect(show_away_players)
    
@login_required(login_url=loginpage)
def show_away_players(request):
    players = away_player.objects.all()
    context = {"players": players}
    return render(request=request, template_name='admin/away/show_away_player.html', context=context)

@login_required(login_url=loginpage)
def add_away_team(request):
    players_data = away_player.objects.all()
    clubs = away_club.objects.all()
    context = {"players": players_data, "clubs": clubs}
    return render(request=request, template_name='admin/away/add_away_team.html', context=context)

@login_required(login_url=loginpage)
def create_away_team(request):
    if request.method == 'POST':
        club_id = request.POST['clubid']
        clubdata = away_club.objects.get(club_id=club_id)
        name = request.POST['name']
        teamdata = away_team(club_id=clubdata, name=name)
        teamdata.save()
        players = [request.POST['player1'], request.POST['player2'], request.POST['player3'], request.POST['player4'], request.POST['player5'], request.POST['player6'], request.POST['player7'], request.POST['player8'], request.POST['player9'], request.POST['player10'], request.POST['player11']]
        for playerdata in players:
            player_data = away_player.objects.get(player_id=playerdata)
            teamplayer_data = away_team_player(team_id=teamdata, player_id=player_data)
            teamplayer_data.save()
        return redirect(show_away_teams)


@login_required(login_url=loginpage)
def show_away_teams(request):
    teamdata = away_team.objects.all()
    teamplayer_data = away_team_player.objects.all()
    players = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    context = {'teams': teamdata, 'teamplayers': teamplayer_data, "players": players}
    return render(request=request, template_name='admin/away/show_away_team.html', context=context)

@login_required(login_url=loginpage)
def edit_away_team_data(request, team_id):
    teamplayers = []
    playernumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    team_data = away_team.objects.get(team_id=team_id)
    players = away_player.objects.all()
    teamplayer_data = away_team_player.objects.filter(team_id=team_data)
    for i, j in zip(teamplayer_data, playernumber):
        tp = []
        tp.append(i.player_id.player_id)
        tp.append(i.player_id.firstname)
        tp.append(i.player_id.lastname)
        tp.append(j)
        teamplayers.append(tp)
    context = {"team": team_data, "teamplayers": teamplayers, "players": players}
    return render(request, template_name='admin/away/edit_away_team.html', context=context)

def update_away_team(request, team_id):
    team_data = away_team.objects.get(team_id=team_id)
    team_data.name = request.POST.get('name')
    team_data.save()
    players = [request.POST.get('player1'), request.POST.get('player2'), request.POST.get('player3'), request.POST.get('player4'), request.POST.get('player5'), request.POST.get('player6'), request.POST.get('player7'), request.POST.get('player8'), request.POST.get('player9'), request.POST.get('player10'), request.POST.get('player11')]
    teamplayer_data = away_team_player.objects.filter(team_id=team_data.team_id)
    for td, p in zip(teamplayer_data, players):
        player_data = away_player.objects.get(player_id=p)
        td.player_id = player_data
        td.save()
    return redirect(show_away_teams)

@login_required(login_url=loginpage) 
def delete_away_team(request, team_id):
    team_data = away_team.objects.get(team_id=team_id)
    team_data.delete()
    return redirect(show_away_teams)

@login_required(login_url=loginpage)
def add_match_data(request):
    home_team = team.objects.all()
    away_team_data = away_team.objects.all()
    context={'home_team': home_team, 'away_team_data': away_team_data}
    return render(request, 'admin/match/add_match.html', context)

@login_required(login_url=loginpage)
def add_match(request):
    if request.method == 'POST':
        name = request.POST['name']
        home_team = request.POST['home_team']
        home = team.objects.get(team_id=home_team)
        away_team_data = request.POST['away_team']
        away = away_team.objects.get(team_id=away_team_data)
        venue = request.POST['venue']
        date = request.POST['date']
        status = request.POST['status']
        matchdata = fixture(name=name, venue=venue, date=date, status=status, team_id=home, away_team_id=away)
        matchdata.save()
        return redirect(show_matches)

@login_required(login_url=loginpage)
def show_matches(request):
    match_data = fixture.objects.all()
    context = {'fixtures': match_data}
    return render(request, 'admin/match/show_matches.html', context)

@login_required(login_url=loginpage)
def edit_match(request, match_id):
    match_data = fixture.objects.get(match_id=match_id)
    date = match_data.date.strftime("%d-%m-%Y")
    print(date)
    team_data = team.objects.all()
    away_data = away_team.objects.all()
    context={'fixture': match_data, 'home': team_data, 'away': away_data, 'date': date}
    return render(request, 'admin/match/edit_match.html', context) 

@login_required(login_url=loginpage)
def update_match(request, match_id):
    match_data = fixture.objects.get(match_id=match_id)
    match_data.name = request.POST['name']
    home_team = request.POST['home_team']
    match_data.team_id = team.objects.get(team_id=home_team)
    away_team_data = request.POST['away_team']
    match_data.away_team_id = away_team.objects.get(team_id=away_team_data)
    match_data.venue = request.POST['venue']
    # match_data.date = request.POST['date']
    match_data.status = request.POST['status']
    match_data.save()
    return redirect(show_matches)

@login_required(login_url=loginpage)
def delete_match(request, match_id):
    match_data = fixture.objects.get(match_id=match_id)
    match_data.delete()
    return redirect(show_matches)