import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

url = "https://www.cars.com/"

driver = webdriver.Chrome()
driver.get(url)

# Pausing execution until you manually proceed
input("Press Enter after you have consented and the page is ready...")

# Get the list of manufacturers
manufacturers = driver.execute_script('''
    const panel = document.querySelector("#panel-19 > cars-search-form");
    const shadowRoot = panel.shadowRoot;
    const form = shadowRoot.querySelector("form > spark-fieldset > spark-select:nth-child(2)");
    const shadowRoot2 = form.shadowRoot;
    const input = shadowRoot2.querySelector("#input");
    const options = Array.from(input.querySelectorAll("option"));
    return options.map(option => option.textContent.trim());
''')

# Remove the "All makes" option
if "All makes" in manufacturers:
    manufacturers.remove("All makes")
time.sleep(2)
# Create a list to store manufacturer and model options
manufacturer_model_pairs = []
all_models = []
for manufacturer in manufacturers:
    # Clear the models list
    model_options = []
    # Selecionar a marca
    select_marca_script = f"""
        const carsSearchForm = document.querySelector("#panel-19 > cars-search-form").shadowRoot;
        const marcaInput = carsSearchForm.querySelector("form > spark-fieldset > spark-select:nth-child(2)").shadowRoot.querySelector("#input");
        marcaInput.value = '{manufacturer}';
        marcaInput.dispatchEvent(new Event('change'));
        """

    driver.execute_script('''
        const panel = document.querySelector("#panel-19 > cars-search-form");
        const shadowRoot = panel.shadowRoot;
        const form = shadowRoot.querySelector("form > spark-fieldset > spark-select:nth-child(2)");
        const shadowRoot2 = form.shadowRoot;
        const input = shadowRoot2.querySelector("#input");
        const option = Array.from(input.querySelectorAll("option")).find(option => option.textContent.trim() === arguments[0]);
        option.selected = true;
        input.dispatchEvent(new Event('change'));
    ''', manufacturer)

    # Get the currently selected manufacturer text
    current_manufacturer = driver.execute_script('''
        const panel = document.querySelector("#panel-19 > cars-search-form");
        const shadowRoot = panel.shadowRoot;
        const form = shadowRoot.querySelector("form > spark-fieldset > spark-select:nth-child(2)");
        const shadowRoot2 = form.shadowRoot;
        const input = shadowRoot2.querySelector("#input");
        return input.options[input.selectedIndex].text.trim();
    ''')

    # Check if the selected manufacturer matches the current loop's manufacturer
    if current_manufacturer.strip() == manufacturer:
        # Wait for the model dropdown to be populated
        WebDriverWait(driver, 100).until(
            lambda driver: len(driver.execute_script('''
                const panel = document.querySelector("#panel-19 > cars-search-form");
                const shadowRoot = panel.shadowRoot;
                let modelDropdown = shadowRoot.querySelector("form > spark-fieldset > spark-select:nth-child(3)");
                let shadowRoot3 = modelDropdown.shadowRoot;
                let modelInput = shadowRoot3.querySelector("#input");
                return Array.from(modelInput.querySelectorAll("option"));
            ''')) > 1
        )

        model_options = driver.execute_script('''
            const panel = document.querySelector("#panel-19 > cars-search-form");
            const shadowRoot = panel.shadowRoot;
            let modelDropdown = shadowRoot.querySelector("form > spark-fieldset > spark-select:nth-child(3)");
            let shadowRoot3 = modelDropdown.shadowRoot;
            let modelInput = shadowRoot3.querySelector("#input");
            const modelOptions = Array.from(modelInput.querySelectorAll("option")).map(option => option.textContent.trim());
            modelOptions.shift(); // Remove the placeholder option
            return modelOptions;
        ''')

        # Add the model options to the list as tuples
        for model_option in model_options:
            manufacturer_model_pairs.append((manufacturer, model_option))
            all_models.append(model_option)
    else:
        # Handle case where manufacturer and model dropdown mismatch (optional)
        print(f"Warning: Mismatch between selected manufacturer {manufacturer} and actual selection {current_manufacturer}")

# Print manufacturer and model options
for pair in manufacturer_model_pairs:
    print(f"Manufacturer: {pair[0]}, Model: {pair[1]}")

# ... your existing code ...

# Print manufacturer and model options and save to CSV
import csv

# ... your existing code ...

# Save manufacturers to CSV
with open('manufacturers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Manufacturer"])  # Writing the header
    for manufacturer in manufacturers:
        writer.writerow([manufacturer])  # Writing the data

# Save manufacturer and model pairs to CSV
with open('manufacturer_model_pairs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Manufacturer", "Model"])  # Writing the headers
    for pair in manufacturer_model_pairs:
        writer.writerow([pair[0], pair[1]])  # Writing the data
with open('models.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Model"])  # Writing the header
    for model in all_models:
        writer.writerow([model])  #