from django.views import generic
from Region.forms import AddRegionForm
from Region.models import Regions
from django.shortcuts import render,redirect


class EditRegion(generic.View):

    def get(self, request, region=None):
        form = AddRegionForm()
        selected_region = None

        edit_region_is_requested = request.GET.get('accion') == 'editar'

        if edit_region_is_requested:
            region_to_edit = Regions.objects.get(pk=region)
            form = form(instance=region_to_edit)
            selected_region = region_to_edit

        context = {
            'form': form,
            'regions': Regions.objects.all(),
            'selected_region': selected_region,
            'title_page': 'Regiones',
            'select_navbar_regions': 1
        }

        return render(request, 'adminEditRegions.html', context)
