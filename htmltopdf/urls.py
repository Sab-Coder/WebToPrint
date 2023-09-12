from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("documents", documents, name="documents"),
    path("matches", matches, name="matches"),
    
    path("upcoming_matches", upcoming_matches, name="upcoming_matches"),
    path("upcoming_match_data/<int:match_id>", upcoming_match_data, name="upcoming_match_data"),
    path("pdf_generate_page/<int:match_id>", pdf_generate_page, name="pdf_generate_page"),
    
    path("view_clubs", view_clubs, name="view_clubs"),
    path("about", about, name="about"),
    path("pdf", generate_pdf, name="pdf"),
    path("test", test, name="test"),
    # authentication
    path("loginpage", loginpage, name="loginpage"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    # admin pages
    path("adminindex", adminindex, name="adminindex"),
    path("add_player", add_player, name="add_player"),
    path("add_player_data", add_player_data, name="add_player_data"),
    path("edit_player_data/<int:player_id>", edit_player_data, name="edit_player_data"),
    path("update_player/<int:player_id>", update_player, name="update_player"),
    path("delete_player/<int:player_id>", delete_player, name="delete_player"),
    path("show_players", show_players, name="show_players"),
    
    path("add_team", add_team, name="add_team"),
    path("create_team", create_team, name="create_team"),
    path("edit_team_data/<int:team_id>", edit_team_data, name="edit_team_data"),
    path("update_team/<int:team_id>", update_team, name="update_team"),
    path("delete_team/<int:team_id>", delete_team, name="delete_team"),
    path("show_teams", show_teams, name="show_teams"),
    
    path("add_club", add_club, name="add_club"),
    path("show_clubs", show_clubs, name="show_clubs"),
    
    
    
    path("add_away_club", add_away_club, name="add_away_club"),
    path("add_awayclub_data", add_awayclub_data, name="add_awayclub_data"),
    path("show_away_club", show_away_club, name="show_away_club"),
    path("edit_away_club/<int:club_id>", edit_away_club, name="edit_away_club"),
    path("update_away_club/<int:club_id>", update_away_club, name="update_away_club"),
    path("delete_away_club/<int:club_id>", delete_away_club, name="delete_away_club"),
    
    path("add_away_player", add_away_player, name="add_away_player"),
    path("add_awayplayer_data", add_awayplayer_data, name="add_awayplayer_data"),
    path("show_away_player", show_away_players, name="show_away_player"),
    path("edit_awayplayer_data/<int:player_id>", edit_awayplayer_data, name="edit_awayplayer_data"),
    path("update_awayplayer/<int:player_id>", update_awayplayer, name="update_awayplayer"),
    path("delete_awayplayer/<int:player_id>", delete_awayplayer, name="delete_awayplayer"),
    
    path("add_away_team", add_away_team, name="add_away_team"),
    path("create_away_team", create_away_team, name="create_away_team"),
    path("show_away_teams", show_away_teams, name="show_away_teams"),
    path("edit_away_team_data/<int:team_id>", edit_away_team_data, name="edit_away_team_data"),
    path("update_away_team/<int:team_id>", update_away_team, name="update_away_team"),
    path("delete_away_team/<int:team_id>", delete_away_team, name="delete_away_team"),
    
    path("add_match_data", add_match_data, name="add_match_data"),
    path("add_match", add_match, name="add_match"),
    path("show_matches", show_matches, name="show_matches"),
    path("edit_match/<int:match_id>", edit_match, name="edit_match"),
    path("update_match/<int:match_id>", update_match, name="update_match"),
    path("delete_match/<int:match_id>", delete_match, name="delete_match"),
    
]