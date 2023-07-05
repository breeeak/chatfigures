from django.urls import re_path
from .views import getNewLabel, getLabelList, export_all_separtions,detect_subfigures,\
    get_figure_separation_results,get_figure_separation_list,figure_separation_upload


urlpatterns = [
    # 检测项目
    re_path(r'^getNewLabel/', getNewLabel),
    re_path(r'^getLabelList/', getLabelList),
    re_path(r'^exportAllSeparations/', export_all_separtions),
    re_path(r'^detectSubfigures/', detect_subfigures),
    re_path(r'^getFigureSeparationResults/', get_figure_separation_results),
    re_path(r'^getFigureSeparationList/', get_figure_separation_list),
    re_path(r'^figureSeparationUpload/', figure_separation_upload),
]

