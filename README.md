# Digital Board

[![Deprecation](https://img.shields.io/badge/deprecation-2.1.0-blue.svg)](https://pypi.org/project/deprecation/)
[![img2pdf](https://img.shields.io/badge/img2pdf-0.4.4-blue.svg)](https://pypi.org/project/img2pdf/)
[![lxml](https://img.shields.io/badge/lxml-4.9.3-blue.svg)](https://pypi.org/project/lxml/)
[![packaging](https://img.shields.io/badge/packaging-23.1-blue.svg)](https://pypi.org/project/packaging/)
[![pikepdf](https://img.shields.io/badge/pikepdf-8.4.1-blue.svg)](https://pypi.org/project/pikepdf/)
[![Pillow](https://img.shields.io/badge/Pillow-9.5.0-blue.svg)](https://pypi.org/project/Pillow/)
[![pyperclip](https://img.shields.io/badge/pyperclip-1.8.2-blue.svg)](https://pypi.org/project/pyperclip/)
[![reportlab](https://img.shields.io/badge/reportlab-4.0.4-blue.svg)](https://pypi.org/project/reportlab/)
[![ttkbootstrap](https://img.shields.io/badge/ttkbootstrap-1.10.1-blue.svg)](https://pypi.org/project/ttkbootstrap/)


The Digital Board project is a Python application that provides a digital canvas for drawing, sketching, and taking notes. It allows users to create and manage multiple slides, draw freehand or use various shapes and tools, add text, change colors, and save their work as PDF files. This README.md file provides an overview of the project, its features, and how to use it.

![Notebook](images/notebook.png)

## Features

### Drawing Tools

The Digital Board application offers the following drawing tools:

- **Pen**: Allows users to draw freehand lines with customizable color and thickness.
- **Eraser**: Erases drawings or text on the canvas.
- **Shapes**: Provides various shapes, including rectangles, circles, squares, lines, arrows, two-faced arrows, and triangles, which users can customize with different colors and sizes.

### Text Tool

Users can add text to the canvas using the "Add Text" option. They can specify the text content, color, size, and font style.

### Color Selection

- Users can choose colors for drawing, text, and background.
- The application provides a palette of recent colors for quick selection.

### Navigation

- Users can navigate between slides, add new slides, and delete existing slides.
- Slides can be saved as PDF files.

### Zoom

- Users can zoom in and out of the canvas using the mouse wheel.

### Context Menu

- Right-clicking on the canvas opens a context menu with options to paste images or add text at the clicked position.

## Requirements

The project requires the following Python libraries to be installed:

- `tkinter` for the GUI components.
- `PIL` (Pillow) for image processing.
- `reportlab` for generating PDF files.
- `img2pdf` for converting images to PDF.
- `pyperclip` for clipboard operations.

## Getting Started

1. Clone or download the project's source code to your local machine.

2. Install the required libraries using `pip` if they are not already installed:

   ```bash
   pip install requirements.txt
   ```

3. Run the `digital_board.py` file:

   ```bash
   python app.py
   ```

4. The Digital Board application will open in fullscreen mode. Use the tools and features as described in the "Features" section.

## Usage

- **Pen Tool**: Select the pen tool to draw freehand lines. Adjust the pen size and color using the toolbar.

- **Eraser Tool**: Select the eraser tool to erase drawings or text. Adjust the eraser size using the toolbar.

- **Shapes**: Choose from various shapes such as rectangles, circles, squares, lines, arrows, two-faced arrows, and triangles. Customize their color and size.

- **Text Tool**: Add text to the canvas by selecting "Add Text" from the context menu. Specify the text content, color, size, and font style.

- **Color Selection**: Use the color chooser to pick colors for drawing, text, and background. Recent colors are available for quick selection.

- **Navigation**: Navigate between slides using the "Previous Slide" and "Next Slide" buttons. Add new slides and delete existing slides as needed.

- **Zoom**: Zoom in and out of the canvas using the mouse wheel.

- **Context Menu**: Right-click on the canvas to access the context menu. You can paste images or add text at the clicked position.

- **Save Slides as PDF**: Save all slides as a PDF file using the "Save as PDF" button in the toolbar. Choose a directory to save image files and specify the PDF file's name and location.

- **Change Background Color**: Right-click on an empty area of the canvas to change the background color.

- **Exit**: Press the `Escape` key or close the application to exit.

## Customization

You can customize the project by replacing the icons and images used in the application. Update the paths to the images and icons in the source code as needed.

## Acknowledgments

The Digital Board project was created using Python and various libraries. Thanks to the contributors and open-source communities of these libraries for their work.

Please note that this project may have additional dependencies, and the requirements might change over time. Ensure that you have the necessary libraries installed to run the application successfully.

For any questions, feedback, or issues related to the Digital Board project, please refer to the project's repository on GitHub or contact the project maintainers.
