'use strict';

let itemId = 0;

/**
 * get the HTML that representing the passed item
 * @param {{id: number, name: string, benefit: number, weight: number}} item the item you want the html for
 * @returns {string} the html that represent the item
 */
const getItemHtml = item =>
  `<div class="flex flex-col ml-2 min-w-[8rem] max-w-[8rem]">
    <input
        type="text"
        name="name.${item.id}"
        id="name.${item.id}"
        autocomplete="item-name"
        class="input"
        onblur="handleChangeItem(${item.id}, 'name', this.value)"
        value="${item.name}"
    />
    <input
        type="number"
        name="benefit.${item.id}"
        id="benefit.${item.id}"
        autocomplete="item-benefit"
        class="input mt-2"
        min="0"
        onblur="handleChangeItem(${item.id}, 'benefit', this.value)"
        value="${item.benefit}"
    />
    <input
        type="number"
        name="weight.${item.id}"
        id="weight.${item.id}"
        autocomplete="item-weight"
        class="input mt-2"
        min="0"
        onblur="handleChangeItem(${item.id}, 'weight', this.value)"
        value="${item.weight}"
    />
    <button class="btn btn-danger mt-2" onclick="handleDeleteItem(${item.id})">Delete</button>
</div>`;

/**
 * get the HTML that representing a log for the passed text
 * @param {string} text the log text
 * @returns {string} the html that represent the log
 */
const getLogHtml = text => `<p>${text}</p>`;

/**
 * get an object that holds an item information
 * @param {number} id item id
 * @param {string} name item name
 * @param {number} benefit item benefit
 * @param {number} weight item weight
 * @returns {{id: number, name: string, benefit: number, weight: number}} object contains the item information
 */
const createItem = (id, name, benefit, weight) => ({ id, name, weight, benefit });

const consoleContainer = document.getElementById('console');
const itemsContainer = document.getElementById('items-container');
const maxWeightInput = document.getElementById('max-weight');
const initialPopulationSizeInput = document.getElementById('initial-population-size');
const mutationProbabilityInput = document.getElementById('mutation-probability');
const eliteInput = document.getElementById('elite');
const timesInput = document.getElementById('times');

let items = [
  createItem(++itemId, '1', 5, 7),
  createItem(++itemId, '2', 8, 8),
  createItem(++itemId, '3', 3, 4),
  createItem(++itemId, '4', 2, 10),
  createItem(++itemId, '5', 7, 4),
  createItem(++itemId, '6', 9, 6),
  createItem(++itemId, '7', 4, 4),
];
let maxWeight = 22;
let initialPopulationSize = 10;
let mutationProbability = 0.4;
let elite = 0.5;
let times = 10;
const syncItems = () => {
  itemsContainer.innerHTML = items.map(item => getItemHtml(item)).join('\n');
};
syncItems();
const syncInputs = () => {
  maxWeightInput.value = maxWeight;
  initialPopulationSizeInput.value = initialPopulationSize;
  mutationProbabilityInput.value = mutationProbability;
  eliteInput.value = elite;
  timesInput.value = times;
};
syncInputs();

const handleDeleteItem = deletedId => {
  items = items.filter(el => el.id !== deletedId);
  syncItems();
};
const handleAddItem = (newId = ++itemId) => {
  items.push(createItem(newId, items.length + 1 + '', 1, 1));
  syncItems();
};
const handleChangeItem = (itemId, prop, newValue) => {
  const index = items.findIndex(item => item.id === itemId);
  if (index === -1) return;
  if (prop === 'name') items[index][prop] = newValue;
  else items[index][prop] = +newValue;
  syncItems();
};

const handleChangeKnapsackMaxWeight = newValue => void (maxWeight = +newValue);
const handleChangeInitialPopulationSize = newValue =>
  void (initialPopulationSize = +newValue);
const handleChangeMutationProbability = newValue =>
  void (mutationProbability = +newValue);
const handleChangeElite = newValue => void (elite = +newValue);
const handleChangeTimes = newValue => void (times = +newValue);

const handleRun = async () => {
  try {
    // use a loading indicator
    consoleContainer.innerHTML = '<p>Running...</p>';

    // sending a request to the server (the problem)
    const response = await fetch('run-code', {
      method: 'POST',
      body: JSON.stringify({
        maxWeight,
        initialPopulationSize,
        mutationProbability,
        elite,
        times,
        items,
      }),
    });
    // if nothing goes wrong
    if (response.ok) {
      // get the json
      const json = await response.json();

      // the logs
      const logs = json.logs;

      // print the logs to the screen
      consoleContainer.innerHTML = logs.map(log => getLogHtml(log)).join('\n');

      // scroll the console to bottom
      consoleContainer.scroll(0, consoleContainer.scrollHeight);
      return;
    }
  } catch (err) {
    console.error(err);
  }

  // print error if something goes wrong
  consoleContainer.innerHTML = `<p style="color: red">Error!</p>`;
};

const handleClear = () => void (consoleContainer.innerHTML = '<p></p>');
