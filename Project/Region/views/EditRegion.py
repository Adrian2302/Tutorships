from django.views import generic
from Region.forms import AddRegionForm
from Region.models import Regions
from django.contrib import messages
from django.shortcuts import render, redirect


class EditRegion(generic.View):

    def get(self, request, region_id=None):
        form = AddRegionForm()
        selected_region = None

        edit_region_is_requested = request.GET.get('accion') == 'editar'

        if edit_region_is_requested:
            region_to_edit = Regions.objects.get(pk=region_id)
            form = AddRegionForm(instance=region_to_edit)
            selected_region = region_to_edit

        context = {
            'form': form,
            'regions': Regions.objects.all(),
            'selected_region': selected_region,
            'title_page': 'Regiones',
            'select_navbar_regions': 1
        }

        return render(request, 'adminEditRegions.html', context)

    def post(self, request, region_id=None):

        form = AddRegionForm(request.POST)
        region_id_is_provided = region_id is not None

        if form.is_valid():
            if region_id_is_provided:
                region_to_edit = Regions.objects.get(pk=region_id)
                region_to_edit.region_name = form.cleaned_data['region_name']
                region_to_edit.country = form.cleaned_data['country']
                region_to_edit.save()
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados exitosamente')
            else:
                form.save()
                messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')
        return redirect('edit_region')
