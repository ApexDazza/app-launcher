# App Launcher

A customizable application launcher with drag-and-drop interface, built with Python and CustomTkinter.

## Features

- Modern, clean interface with customizable buttons
- Drag-and-drop functionality for button arrangement
- Dark mode theme
- Keyboard shortcuts for quick actions
- Configuration persistence
- Analytics tracking (optional)

## Installation

### From Source
1. Clone the repository:
```bash
git clone https://github.com/ApexDazza/app-launcher.git
cd app-launcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python launcher.py
```

### From Executable
1. Download the latest release from the [releases page](https://github.com/ApexDazza/app-launcher/releases)
2. Run the installer
3. Launch from the desktop shortcut or start menu

## Usage

### Basic Usage
- Click any button to launch the associated application or website
- Use the Edit button (or Ctrl+E) to enter edit mode
- In edit mode, drag buttons to rearrange them
- Click Done or press Ctrl+E again to exit edit mode

### Keyboard Shortcuts
- `Ctrl+E`: Toggle edit mode
- `Ctrl+S`: Save current layout
- `Ctrl+R`: Refresh layout

### Configuration
The app stores its configuration in:
- `layout.json`: Button arrangement
- `analytics.json`: Usage statistics (if enabled)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components
- All contributors and users of this application
