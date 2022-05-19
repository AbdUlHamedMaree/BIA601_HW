let itemId = 0;
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
const getLogHtml = text => `<p>${text}</p>`;

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
let mutationProbability = 0.3;
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
    consoleContainer.innerHTML = '<p>Running...</p>';
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
    if (response.ok) {
      const json = await response.json();
      logs = json.logs;
      consoleContainer.innerHTML = logs.map(log => getLogHtml(log)).join('\n');
      consoleContainer.scroll(0, consoleContainer.scrollHeight);
      return;
    }
  } catch (err) {}
  consoleContainer.innerHTML = `<p style="color: red">Error!</p>`;
};

const handleClear = () => void (consoleContainer.innerHTML = '<p></p>');
