import django.http
import folium
from django.shortcuts import render
from pokemon_entities.models import Pokemon
from django.utils.timezone import localtime

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_photo = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_photo,
            'title_ru': pokemon.title,
        })

        get_pokemons_entity(pokemon, folium_map, pokemon_photo)

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except django.http.Http404:
        raise '<h1>Такой покемон не найден</h1>'
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    if pokemon.id == int(pokemon_id):
        pokemon_photo = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL
        pokemon_details = {
            'img_url': pokemon_photo,
            'title_ru': pokemon.title,
            'description': pokemon.description,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
        }

        get_pokemons_entity(pokemon, folium_map, pokemon_photo)
        get_next_evolution(request, pokemon, pokemon_details)
        get_previous_evolution(request, pokemon, pokemon_details)

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_details
    })


def get_pokemons_entity(pokemon, folium_map, pokemon_photo):
    pokemons_entity = pokemon.entities.filter(appeared_at__lt=localtime().now(),
                                              disappeared_at__gt=localtime().now())
    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_photo,
        )


def get_next_evolution(request, pokemon, pokemon_details):
    pokemon = pokemon.next_evolution.all().first()
    if pokemon:
        pokemon_photo = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL
        pokemon_details['next_evolution'] = {
            "title_ru": pokemon.title,
            "pokemon_id": pokemon.id,
            "img_url": pokemon_photo
        }


def get_previous_evolution(request, pokemon, pokemon_details):
    pokemon = pokemon.previous_evolution
    if pokemon:
        pokemon_photo = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL
        pokemon_details['previous_evolution'] = {
            "title_ru": pokemon.title,
            "pokemon_id": pokemon.id,
            "img_url": pokemon_photo
        }
