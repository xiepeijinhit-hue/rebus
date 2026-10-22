'use strict';
const SUBSETS = [
  ['en_emoji', 'English Emoji'], ['en_image', 'English Pictorial'],
  ['zh_emoji', 'Chinese Idiom'], ['zh_image', 'Chinese Pictorial'],
];
const $ = id => document.getElementById(id);
const state = { rows: [], subset: 'all', page: 1, revealed: new Set(), ready: false };
function element(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
}
function filteredRows() {
  const keyword = $('search').value.trim().toLowerCase();
  const count = $('imageFilter').value;
  return state.rows.filter(row =>
    (state.subset === 'all' || row.subset === state.subset) &&
    (count === 'all' || [row.image_1, row.image_2].filter(Boolean).length === Number(count)) &&
    (!keyword || [row.uid, row.source_id, row.emoji, row.hint, row.prompt].join(' ').toLowerCase().includes(keyword))
  );
}
function makeCard(row) {
  const card = element('article', 'card');
  card.dataset.uid = row.uid;
  const top = element('div', 'card-top');
  top.append(element('span', 'pill', SUBSETS.find(([key]) => key === row.subset)[1]), element('span', 'card-id', row.uid));
  const visuals = element('div', 'visuals');
  const images = [row.image_1, row.image_2].filter(Boolean);
  if (!images.length) {
    const emoji = element('div', 'emoji', row.emoji);
    emoji.setAttribute('aria-label', `Puzzle symbols: ${row.emoji}`);
    visuals.append(emoji);
  }
  images.forEach((path, index) => {
    const button = element('button', 'image-button');
    button.type = 'button';
    button.setAttribute('aria-label', `Enlarge ${row.uid} image ${index + 1}`);
    const image = element('img');
    image.src = path;
    image.alt = `${row.uid} — figure ${index + 1}`;
    image.loading = 'lazy';
    image.decoding = 'async';
    image.addEventListener('error', () => { image.alt = 'Preview unavailable'; });
    button.append(image, element('span', '', `FIG ${index + 1}`));
    button.addEventListener('click', () => {
      $('zoomImage').src = path;
      $('zoomImage').alt = image.alt;
      $('zoomCaption').textContent = `${image.alt} · reduced-size preview, not evaluation input`;
      $('zoom').showModal();
    });
    visuals.append(button);
  });
  const body = element('div', 'card-body');
  if (row.hint) body.append(element('p', 'hint', `FIG 1 HINT · ${row.hint}`));
  const prompt = element('p', 'prompt', row.prompt);
  prompt.lang = row.language;
  body.append(prompt);
  const reveal = element('button', 'reveal');
  reveal.type = 'button';
  const answer = element('div', 'answer');
  answer.id = `answer-${row.uid}`;
  answer.lang = row.language;
  answer.append(element('small', '', 'REFERENCE ANSWER · 原始参考答案'), element('span', '', row.answer));
  reveal.setAttribute('aria-controls', answer.id);
  function updateAnswer() {
    const visible = $('showAnswers').checked || state.revealed.has(row.uid);
    answer.hidden = !visible;
    reveal.textContent = visible ? 'Hide answer / 隐藏答案' : 'Show answer / 查看答案';
    reveal.setAttribute('aria-expanded', String(visible));
  }
  reveal.addEventListener('click', () => {
    if ($('showAnswers').checked) {
      $('showAnswers').checked = false;
      state.revealed.delete(row.uid);
      render();
      return;
    }
    state.revealed.has(row.uid) ? state.revealed.delete(row.uid) : state.revealed.add(row.uid);
    updateAnswer();
  });
  updateAnswer();
  body.append(reveal, answer);
  card.append(top, visuals, body);
  return card;
}
function render() {
  if (!state.ready) return;
  const rows = filteredRows();
  const size = Number($('pageSize').value);
  const pages = Math.max(1, Math.ceil(rows.length / size));
  state.page = Math.min(state.page, pages);
  $('cards').replaceChildren(...rows.slice((state.page - 1) * size, state.page * size).map(makeCard));
  $('empty').hidden = rows.length !== 0;
  $('status').textContent = `${rows.length} matching samples · ${state.rows.length} in this snapshot · search does not inspect answers`;
  $('pageInfo').textContent = `Page ${state.page} of ${pages}`;
  $('prev').disabled = state.page === 1;
  $('next').disabled = state.page === pages;
  $('download').disabled = rows.length === 0;
  $('tabs').querySelectorAll('button').forEach(btn => btn.setAttribute('aria-pressed', String(btn.dataset.subset === state.subset)));
}
function resetPage() { state.page = 1; render(); }
$('search').addEventListener('input', resetPage);
['imageFilter', 'pageSize', 'showAnswers'].forEach(id => $(id).addEventListener('change', resetPage));
$('reset').addEventListener('click', () => {
  state.subset = 'all'; $('search').value = ''; $('imageFilter').value = 'all';
  $('showAnswers').checked = false; state.revealed.clear(); resetPage();
});
['prev', 'next'].forEach(id => $(id).addEventListener('click', () => { state.page += id === 'next' ? 1 : -1; render(); $('explore').scrollIntoView(); }));
$('download').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(filteredRows(), null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = element('a'); link.href = url; link.download = `birebus-${state.subset}-preview.json`;
  link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
$('closeZoom').addEventListener('click', () => $('zoom').close());
$('zoom').addEventListener('click', e => { if (e.target === $('zoom')) $('zoom').close(); });
async function load() {
  try {
    const datasets = await Promise.all(SUBSETS.map(async ([name]) => {
      const response = await fetch(`data/${name}.json`);
      if (!response.ok) throw new Error(`${name}: HTTP ${response.status}`);
      return response.json();
    }));
    const max = Math.max(...datasets.map(rows => rows.length));
    for (let i = 0; i < max; i++) for (const rows of datasets) if (rows[i]) state.rows.push(rows[i]);
    const options = [['all', 'All subsets'], ...SUBSETS];
    $('tabs').replaceChildren(...options.map(([key, label]) => {
      const count = state.rows.filter(r => key === 'all' || r.subset === key).length;
      const btn = element('button', 'tab', `${label} · ${count}`);
      btn.dataset.subset = key;
      btn.addEventListener('click', () => { state.subset = key; resetPage(); });
      return btn;
    }));
    state.ready = true;
    $('sampleCount').textContent = state.rows.length;
    $('imageCount').textContent = state.rows.reduce((n, r) => n + Number(Boolean(r.image_1)) + Number(Boolean(r.image_2)), 0);
    render();
  } catch (error) {
    $('status').textContent = 'Unable to load dataset.';
    $('error').hidden = false;
    $('error').textContent = `Open this directory through an HTTP server, not file://. ${error.message}`;
    $('prev').disabled = $('next').disabled = true;
  }
}
load();
