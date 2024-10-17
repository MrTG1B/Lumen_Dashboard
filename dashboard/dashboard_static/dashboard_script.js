// Get all the radio buttons
const radioButtons = document.querySelectorAll('input[name="radio"]');

// Add an event listener to each radio button
radioButtons.forEach((radio) => {
    radio.addEventListener('change', () => {
        if (radio.checked) {
            // Get the label (img alt attribute) corresponding to the checked radio button
            const label = radio.nextElementSibling.getAttribute('alt');
            if (label === 'faulty') {
                document.getElementById('allLightsContainer').style.display = 'none';
                document.getElementById('faultyLightsContainer').style.display = 'flex';
            } else {
                document.getElementById('allLightsContainer').style.display = 'flex';
                document.getElementById('faultyLightsContainer').style.display = 'none';
            }
        }
    });
});

document.getElementById('faultySearchBtn').addEventListener('click', function() {
    this.classList.toggle('clicked');

    // Store the reference to the button
    const button = this;

    // button.style.
    
    let areaName = '';
    const lightListContainer = document.getElementById('faultyLightNameList');
    // Clear the container
    lightListContainer.innerHTML = '';

    const areaRadio= document.querySelectorAll('input[name="arearadio"]');

    areaRadio.forEach((radio) => {
        if (radio.checked) {
            const label = radio.nextElementSibling;
            areaName = label.textContent;
            console.log(areaName);
            // createFaultyLightListButtons(areaName);
        }
    });
    

    
    // Remove the 'clicked' class after 10 seconds (10000 milliseconds)
    setTimeout(function() {
        button.classList.remove('clicked');
        createFaultyLightListButtons(areaName)
    }, 10000);
});

const timeText = document.getElementById("timeText");
const dateText = document.getElementById("dateText");

function updateClock() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    
    // Convert to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'

    // Format time
    timeText.textContent = `${hours}:${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

    // Format AM/PM
    ampmText.textContent = ampm;

    // Format date
    const day = now.getDate();
    const options = { weekday: 'long', month: 'long' };
    const formattedDate = now.toLocaleDateString(undefined, options);

    // Get the appropriate suffix
    const suffix = getDaySuffix(day);

    // Set the formatted date with the day and suffix
    dateText.innerHTML = `${formattedDate} ${day}<sup>${suffix}</sup>`;
}

function getDaySuffix(day) {
    if (day >= 11 && day <= 13) {
        return 'th';
    }
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}

setInterval(updateClock, 1000);

function setGaugeValue(value,background,percentage,color) {
    // Update the percentage text
    percentage.innerText = value;

    // Map the value to an angle (from 0 to 360 degrees)
    const angle = (value / 100) * 360;

    // Apply the conic-gradient to create the arc, with the red span covering from 0 to the calculated angle
    background.style.background = `conic-gradient(${color} 0deg ${angle}deg, transparent ${angle}deg 360deg)`;
}
const energyConsumptionBar = document.getElementById('energyConsumptionBar');
const totalEnergyConsumptionText = document.getElementById('totalEnergyConsumptionText');
setInterval(() => setGaugeValue(Math.floor(Math.random() * 100),energyConsumptionBar,totalEnergyConsumptionText,"red"), 1000);

const energySavedBar = document.getElementById('energySavedBar');
const totalEnergySavedText = document.getElementById('totalEnergySavedText');
setInterval(() => setGaugeValue(Math.floor(Math.random() * 100),energySavedBar,totalEnergySavedText,"green"), 10000);



function createRadioList(mode,text_list,listId,radioClassName,textClassName) {
    const lightListContainer = document.getElementById(listId);

    // Clear the container
    lightListContainer.innerHTML = '';

    if (text_list.length === 0) {
        const text = document.createElement('p');
        if (mode === 0) {
            text.innerHTML = "No Area Found";
        } else {
            text.innerHTML = "No Lights Found";
        }
        text.className = textClassName;
        text.style.color = '#F6F3ED';
        text.style.textAlign = 'center';
        text.style.fontSize = '16px';
        lightListContainer.appendChild(text);
        return;
    }

    // Dynamically create a radio button for each light
    text_list.forEach((light, index) => {
        // Create the label element with class 'lightradio'
        const label = document.createElement('label');
        label.className = radioClassName;

        // Create the radio input element
        const radioInput = document.createElement('input');
        radioInput.type = 'radio';
        radioInput.name = radioClassName; // All radio buttons should share the same name
        if (index === 0 && mode === 0) {
            radioInput.checked = true; // Set the first radio button as checked
            getMap(light);
            createLightListButtons(light);
            createFaultyLightListButtons(light);
        }

        const text = document.createElement('p');
        text.innerHTML = light;
        text.className = textClassName;
        text.style.color = radioInput.checked ? 'black' : 'white'; // Initial color for the first button

        // Append the radio input and text to the label
        label.appendChild(radioInput);
        label.appendChild(text);

        // Append the label to the lightNameList container
        lightListContainer.appendChild(label);
    });

    // Add event listeners to the newly created radio buttons
    const lightListRadioButtons = document.querySelectorAll('input[name="'+radioClassName+'"]');
    lightListRadioButtons.forEach((radio) => {
        radio.addEventListener('change', () => {
            lightListRadioButtons.forEach((btn) => {
                // Set the color of all text elements to white (unselected)
                const label = btn.nextElementSibling;
                label.style.color = 'white';
            });

            let areaName = '';

            const areaRadio= document.querySelectorAll('input[name="arearadio"]');

            areaRadio.forEach((radio1) => {
                if (radio1.checked) {
                    const label = radio1.nextElementSibling;
                    areaName = label.textContent;
                    console.log(areaName);
                    // createFaultyLightListButtons(areaName);
                }
            });
            
            // Set the color of the selected radio button's text to black
            if (radio.checked) {
                const label = radio.nextElementSibling;
                label.style.color = 'black';
                if (mode === 0) {
                    getMap(label.textContent);
                    createLightListButtons(label.textContent);
                    createFaultyLightListButtons(label.textContent); // Calling the function
                }
                else if (mode === 1) {
                    createLightPostMap(label.textContent,areaName);
                }
            }
        });
    });
}

async function createLightPostMap(light, area) {
    try {
        // Encode 'light' and 'area' to handle special characters like '/'
        const encodedLight = encodeURIComponent(light);
        const encodedArea = encodeURIComponent(area);

        // Construct the URL using the encoded values
        const response = await fetch(`https://6883cjlh-8080.inc1.devtunnels.ms/${encodedArea}/${encodedLight}/location_src`);
        
        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Get the text data from the response
        const data = await response.text();

        // Set the src of the map iframe
        const map = document.getElementById('map');
        map.src = data;
    } catch (error) {
        console.error('Error fetching src:', error);
    }
}

async function createAreaListButtons() {
    try {
        // Fetch the data from the Flask server's /arealist endpoint
        const response = await fetch('https://6883cjlh-8080.inc1.devtunnels.ms/arealist');
        
        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Get the text data (assuming the area list is in plain text, one per line)
        const data = await response.text();

        // Split the text into an array of area names (assuming new line delimited)
        const areas = data.split('\n').filter(Boolean); // Remove empty lines

        createRadioList(0,areas,'areaNameList','arearadio','areaname');

        const areaNameInput= document.getElementById('areaNameInput');
        areaNameInput.addEventListener('input', () => {
            const inputValue = areaNameInput.value;
            const filteredAreas = areas.filter(area => area.toLowerCase().includes(inputValue.toLowerCase()));
            createRadioList(0,filteredAreas,'areaNameList','arearadio','areaname');
        });

       
    } catch (error) {
        console.error('Error fetching area list:', error);
    }
}

async function createLightListButtons(areaName) {
    try {
        // Fetch the data from the Flask server's /lightlist endpoint
        const response = await fetch('https://6883cjlh-8080.inc1.devtunnels.ms/area/'+ areaName+'/lp');
        
        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Get the text data (assuming the light list is in plain text, one per line)
        const data = await response.text();

        // Split the text into an array of light names (assuming new line delimited)
        const lights = data.split('\n').filter(Boolean); // Remove empty lines

        createRadioList(1,lights,'lightNameList','lightradio','lightname');

        const lightNameInput= document.getElementById('lightNameInput');

        lightNameInput.addEventListener('input', () => {
            const inputValue = lightNameInput.value;
            const filteredLights = lights.filter(light => light.toLowerCase().includes(inputValue.toLowerCase()));
            createRadioList(1,filteredLights,'lightNameList','lightradio','lightname');
            
        });        
    } catch (error) {
        console.error('Error fetching light list:', error);
    }
}

async function createFaultyLightListButtons(areaName) {
    try{
        const response = await fetch('https://6883cjlh-8080.inc1.devtunnels.ms/area/'+ areaName+'/faulty_lp');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const lightListContainer = document.getElementById('faultyLightNameList');

        // Clear the container
        lightListContainer.innerHTML = '';

        if (response.status === 204) {
            const text = document.createElement('p');
            text.innerHTML = "No Faulty Lights";
            text.className = 'falutylightname';
            text.style.color = '#F6F3ED';
            text.style.textAlign = 'center';
            text.style.fontSize = '16px';
            lightListContainer.appendChild(text);
            return;
        }
        else if (response.status === 200) {
            const data = await response.text();
            const lights = data.split('\n').filter(Boolean); // Remove empty lines
            createRadioList(1,lights,'faultyLightNameList','falutylightradio','falutylightname');

            const faultyLightNameInput= document.getElementById('faultyLightNameInput');

            faultyLightNameInput.addEventListener('input', () => {
                const inputValue = faultyLightNameInput.value;
                const filteredLights = lights.filter(light => light.toLowerCase().includes(inputValue.toLowerCase()));
                createRadioList(1,filteredLights,'faultyLightNameList','falutylightradio','falutylightname');
            });
        }
    } catch (error) {
        console.error('Error fetching light list:', error);
    }
}

async function getMap(areaName) {
    try{
        const response = await fetch('https://6883cjlh-8080.inc1.devtunnels.ms/area/'+ areaName+'/map');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.text();
        const map= document.getElementById('map');
        map.src = data;
        map.onload = function() {
            console.log('Map loaded successfully');
        };
    }catch (error) {
        console.error('Error fetching src:', error);
    }
}

// Call the function to create buttons when the page loads
window.onload = function() {
    setTimeout(function() {
        createAreaListButtons();
    }, 2000);
}
