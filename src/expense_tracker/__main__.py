# Tema: ejecución del paquete desde la terminal.

from expense_tracker.cli import main

# SystemExit entrega a la terminal el código de éxito o error que devuelve la interfaz.
raise SystemExit(main())
