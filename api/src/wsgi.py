import logging
import app as main_module

app = main_module.main()


if __name__ == "__main__":
    # Disable flask logs
    app.logger.disabled = True
    log = logging.getLogger("werkzeug")
    log.disabled = True

    app.run(debug=True)
