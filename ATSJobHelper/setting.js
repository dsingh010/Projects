// settings.js

document.getElementById('saveApiKey').addEventListener('click', () => {
  const apiKey = document.getElementById('apiKeyInput').value;
  const apiService = document.getElementById('apiServiceSelect').value;
  const model = document.getElementById('modelSelect').value;
  console.log('Saving model:', model); // Debug log
  chrome.storage.sync.set({ apiKey, apiService, model }, () => {
    alert('API key, service, and model saved!');
  });
});

// Filter models based on selected service
const apiServiceSelect = document.getElementById('apiServiceSelect');
const modelSelect = document.getElementById('modelSelect');

function filterModels() {
  const service = apiServiceSelect.value;
  Array.from(modelSelect.options).forEach(option => {
    const services = option.getAttribute('data-service').split(' ');
    option.style.display = services.includes(service) ? '' : 'none';
  });
  // Select the first visible option
  const firstVisible = Array.from(modelSelect.options).find(option => option.style.display !== 'none');
  if (firstVisible) {
    modelSelect.value = firstVisible.value;
    modelSelect.dispatchEvent(new Event('change'));
  }
}

apiServiceSelect.addEventListener('change', filterModels);

// Load saved model/service/key on modal open
window.addEventListener('DOMContentLoaded', () => {
  chrome.storage.sync.get(['apiKey', 'apiService', 'model'], (result) => {
    document.getElementById('apiKeyInput').value = result.apiKey || '';
    apiServiceSelect.value = result.apiService || 'groq';
    filterModels();
    modelSelect.value = result.model || modelSelect.value;
    console.log('Loaded model:', modelSelect.value); // Debug log
  });
}); 
