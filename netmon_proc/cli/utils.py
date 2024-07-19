def yaspin_terminator(*_, spinner):
    spinner.hide()
    spinner.stop()
    raise KeyboardInterrupt
