from django.urls import re_path
from .views import detect_scale_bars, get_results, initMeasureImage, measureAnythingPoint, \
    interactive_measurement_upload


urlpatterns = [
    # 检测项目
    re_path(r'^detect/', detect_scale_bars),
    re_path(r'^getResults/', get_results),
    re_path(r'^initMeasureImage/', initMeasureImage),
    re_path(r'^measureAnythingPoint/', measureAnythingPoint),
    re_path(r'^interactiveMeasurementUpload/', interactive_measurement_upload),

]
