from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement

def character_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'snails/character_list.html', {'characters': characters, 'equipements':equipements})
    
def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    equipement = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)

    form = MoveForm(request.POST, instance=character)
    
    if form.is_valid():
        ancien_lieu = equipement
        ancien_lieu.disponibilite = "libre"
        ancien_lieu.save()

        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        
        if nouveau_lieu.disponibilite == "occupé":
            return render(request, 'snails/occupe.html', {})
        
        else:
            if nouveau_lieu.id_equip == "sol":
                nouveau_lieu.disponibilite = "libre"
            else:
                nouveau_lieu.disponibilite = "occupé"
                
            nouveau_lieu.save()
            
            character.lieu = nouveau_lieu
            character.save()

            return redirect('character_detail', id_character=id_character)

    return render(request, 'snails/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form})



def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    return render(request, 'snails/equipement_detail.html', {'equipement': equipement})
