# features/environment.py
def after_scenario(context, scenario):
    # Nettoyer les patchs après chaque scénario
    if hasattr(context, 'patches'):
        for patch in context.patches:
            patch.stop()
