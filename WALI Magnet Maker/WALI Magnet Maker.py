import os
import csv
import traceback
import adsk.core
import adsk.fusion


# CONSTANTS
SKETCH_NAME = "wali-text"


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        doc = app.activeDocument

        ui.messageBox(f"Active document: {doc.name}")

        # Load your CSV
        script_dir = os.path.dirname(__file__)
        csv_path = os.path.join(script_dir, 'stickers.csv')

        # return if CSV not found
        if not os.path.exists(csv_path):
            ui.messageBox(f"CSV not found at: {csv_path}")
            return

        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            names = [row['text'] for row in reader]

        # return if csv is empty
        if not names:
            ui.messageBox("No names found in CSV.")
            return

        root_comp = design.rootComponent
        sketches = root_comp.sketches

        # find sketch that matches sketch name.
        sketch = None
        for s in sketches:
            if s.name == SKETCH_NAME:  # <== your chosen name here
                sketch = s
                break

        if sketch is None:
            ui.messageBox(f"Could not find sketch named '{SKETCH_NAME}'.")
            return
        
        # check there is text in your sketch.
        texts = sketch.sketchTexts
        if texts.count == 0:
            ui.messageBox("No sketch text objects found in 'TextSketch'")
            return
        
        text_item = texts.item(0)  # assumes one text object in the sketch

        for name in names:
            # Update the text
            text_item.text = name

            # Force compute to regenerate the geometry
            design.timeline.moveToEnd()


            # Generate unique filename if needed
            base_path = os.path.join(script_dir, f'magnets/{name}.step')
            step_path = base_path
            suffix = 1
            while os.path.exists(step_path):
                step_path = os.path.join(script_dir, f'{name}_{suffix}.step')
                suffix += 1

            # Export
            export_mgr = design.exportManager
            step_options = export_mgr.createSTEPExportOptions(step_path)
            export_mgr.execute(step_options)


        ui.messageBox('All STEP files exported successfully.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
