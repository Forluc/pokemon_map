import folium
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity
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
    time_now = localtime().now()

    for pokemon in pokemons:
        pokemon_photo = get_pokemon_photo(request, pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_photo,
            'title_ru': pokemon.title,
        })

    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lt=time_now, disappeared_at__gt=time_now)

    for pokemon_entity in pokemons_entity:
        pokemon_photo = get_pokemon_photo(request, pokemon_entity.pokemon)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_photo,
        )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    chosen_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_photo = get_pokemon_photo(request, chosen_pokemon)
    pokemon_details = {
        'img_url': pokemon_photo,
        'title_ru': chosen_pokemon.title,
        'description': chosen_pokemon.description,
        'title_en': chosen_pokemon.title_en,
        'title_jp': chosen_pokemon.title_jp,
    }

    time_now = localtime().now()
    pokemons_entity = chosen_pokemon.entities.filter(appeared_at__lt=time_now,
                                                     disappeared_at__gt=time_now)
    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_photo,
        )

    pokemon = chosen_pokemon.next_evolutions.first()
    if pokemon:
        pokemon_photo = get_pokemon_photo(request, pokemon)
        pokemon_details['next_evolution'] = {
            "title_ru": pokemon.title,
            "pokemon_id": pokemon.id,
            "img_url": pokemon_photo
        }

    pokemon = chosen_pokemon.previous_evolution
    if pokemon:
        pokemon_photo = get_pokemon_photo(request, pokemon)
        pokemon_details['previous_evolution'] = {
            "title_ru": pokemon.title,
            "pokemon_id": pokemon.id,
            "img_url": pokemon_photo
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_details
    })


def get_pokemon_photo(request, pokemon):
    return request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL
