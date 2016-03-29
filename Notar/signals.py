def mediafile_delete(sender, instance, **kwargs):
    """
    Signal receiver to delete a mediafile on the filesystem.
    """
    # Pass False so FileField doesn't save the model.
    instance.mediafile.delete(save=False)
