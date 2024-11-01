from .views import podcast_chooser_viewset

PodcastChooserBlock = podcast_chooser_viewset.get_block_class(
    name="PodcastChooserBlock", module_path="podcast.blocks"
)