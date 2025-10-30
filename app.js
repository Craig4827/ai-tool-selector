
// Simple client-side app that loads data/tools.json
async function init() {
  const res = await fetch('data/tools.json');
  const data = await res.json();
  window.toolData = data;

  const functionSelect = document.getElementById('functionSelect');
  const toolTypeSelect = document.getElementById('toolTypeSelect');
  const toolTypeArea = document.getElementById('toolTypeArea');
  const recommendations = document.getElementById('recommendations');
  const toolList = document.getElementById('toolList');

  // populate functions
  Object.keys(data).forEach(fn => {
    const opt = document.createElement('option');
    opt.value = fn;
    opt.textContent = fn;
    functionSelect.appendChild(opt);
  });

  functionSelect.addEventListener('change', () => {
    const fn = functionSelect.value;
    toolTypeSelect.innerHTML = '<option value="">-- select a tool type --</option>';
    toolList.innerHTML = '';
    recommendations.classList.add('hidden');

    if (!fn) {
      toolTypeArea.classList.add('hidden');
      return;
    }
    const types = Object.keys(data[fn]['AI Tool Types']);
    types.forEach(t => {
      const opt = document.createElement('option');
      opt.value = t;
      opt.textContent = t;
      toolTypeSelect.appendChild(opt);
    });
    toolTypeArea.classList.remove('hidden');
  });

  toolTypeSelect.addEventListener('change', () => {
    const fn = functionSelect.value;
    const tt = toolTypeSelect.value;
    toolList.innerHTML = '';
    if (!tt) {
      recommendations.classList.add('hidden');
      return;
    }
    const tools = data[fn]['AI Tool Types'][tt];
    tools.forEach(tool => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = tool.url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.textContent = tool.name;
      li.appendChild(a);
      toolList.appendChild(li);
    });
    recommendations.classList.remove('hidden');
  });
}

window.addEventListener('DOMContentLoaded', init);
