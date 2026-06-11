/* Foundry kanban — unified filter for hub + skill pages. No behavioural differences. */
(function () {
  'use strict';

  var FILTER_KEY = 'abd-foundry-skill-nav-filter';
  var SKILLS_EXPANDED_KEY = 'abd-foundry-skill-page-skills-expanded';
  var CROSSCUT_KEY = 'abd-foundry-skill-nav-crosscut';

  function readSavedFilter() {
    try {
      var raw = window.sessionStorage.getItem(FILTER_KEY);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      var families = Array.isArray(parsed.families) ? parsed.families : [];
      if (parsed.other && families.indexOf('other') === -1) families.push('other');
      return { families: families };
    } catch (err) { return null; }
  }

  function saveFilter(families) {
    try {
      window.sessionStorage.setItem(FILTER_KEY, JSON.stringify({ families: families }));
    } catch (err) {}
  }

  function readSkillsExpandedPref() {
    try { return window.sessionStorage.getItem(SKILLS_EXPANDED_KEY) === '1'; }
    catch (err) { return false; }
  }

  function saveSkillsExpandedPref(expanded) {
    try { window.sessionStorage.setItem(SKILLS_EXPANDED_KEY, expanded ? '1' : '0'); }
    catch (err) {}
  }

  function readCrosscutPref() {
    try {
      var raw = window.sessionStorage.getItem(CROSSCUT_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed.groups) ? parsed.groups : [];
    } catch (err) { return []; }
  }

  function saveCrosscutPref(groups) {
    try {
      window.sessionStorage.setItem(CROSSCUT_KEY, JSON.stringify({ groups: groups }));
    } catch (err) {}
  }

  function familyFromTicket(link) {
    var row = link.closest('.aad-skill-row[data-family]');
    return row ? row.getAttribute('data-family') : null;
  }

  function collectSelectedFamilies(surface) {
    var out = [];
    surface.querySelectorAll('.foundry-family-toggle.is-selected').forEach(function (btn) {
      var f = btn.getAttribute('data-family');
      if (f && out.indexOf(f) === -1) out.push(f);
    });
    return out;
  }

  function pageBasename() {
    var path = window.location.pathname || '';
    var parts = path.split('/');
    return parts[parts.length - 1].split('?')[0] || '';
  }

  function stageFromUrl() {
    try { return new URLSearchParams(window.location.search).get('stage') || ''; }
    catch (err) { return ''; }
  }

  function parseSkillHref(href) {
    if (!href) return { base: '', stage: '' };
    var q = href.indexOf('?');
    var base = q >= 0 ? href.slice(0, q) : href;
    var stage = '';
    if (q >= 0) {
      try { stage = new URLSearchParams(href.slice(q)).get('stage') || ''; } catch (err) {}
    }
    return { base: base, stage: stage };
  }

  function buildStageUrl(stageId) {
    var page = pageBasename();
    return stageId ? page + '?stage=' + encodeURIComponent(stageId) : page;
  }

  /* Save filter before navigating away */
  document.querySelectorAll('.foundry-kanban-surface').forEach(function (surf) {
    surf.querySelectorAll('a.kb-ticket.aad-skill[href]').forEach(function (link) {
      if (link.classList.contains('foundry-practice-col__card')) return;
      if (link.classList.contains('aad-crosscut-row-title')) return;
      link.addEventListener('click', function (e) {
        var ticketFamily = familyFromTicket(link);
        var families = collectSelectedFamilies(surf);
        var parsed = parseSkillHref(link.getAttribute('href') || '');
        if (parsed.base === pageBasename() && parsed.stage) {
          e.preventDefault();
          if (ticketFamily && families.indexOf(ticketFamily) === -1) families.push(ticketFamily);
          saveFilter(families);
          if (window.history && window.history.pushState) {
            window.history.pushState({ foundryStage: parsed.stage }, '', buildStageUrl(parsed.stage));
          }
          if (typeof window.__foundryApplyStage === 'function') window.__foundryApplyStage(parsed.stage);
          return;
        }
        if (ticketFamily && families.indexOf(ticketFamily) === -1) families.push(ticketFamily);
        if (!families.length && ticketFamily) families = [ticketFamily];
        saveFilter(families);
      });
    });
  });

  /* ── Filter logic — identical for hub and skill pages ── */
  var surface = document.querySelector('.foundry-kanban-surface');
  if (!surface) return;

  surface.classList.add('foundry-skill-nav-settling');

  var familyButtons = Array.prototype.slice.call(surface.querySelectorAll('.foundry-family-toggle'));
  var skillsToggle = document.getElementById('foundry-skills-toggle');
  var skillsExpanded = false;
  var colHeads = Array.prototype.slice.call(surface.querySelectorAll('.kb-col-head[data-stage]'));
  var rows = Array.prototype.slice.call(surface.querySelectorAll('.kb-col > .aad-skill-row[data-family]'));
  var stageSkillRows = Array.prototype.slice.call(surface.querySelectorAll('.foundry-stage-skills'));
  var crosscutPracticeRows = Array.prototype.slice.call(
    surface.querySelectorAll('.aad-delivery-crosscut-section--supporting .aad-delivery-crosscut-row')
  );
  var crosscutOtherRows = Array.prototype.slice.call(
    surface.querySelectorAll('.aad-delivery-crosscut-section--foundational .aad-delivery-crosscut-row')
  );
  var crosscutToggles = Array.prototype.slice.call(surface.querySelectorAll('.aad-crosscut-row-toggle'));
  var supportingSection = surface.querySelector('.aad-delivery-crosscut-section--supporting');
  var foundationalSection = surface.querySelector('.aad-delivery-crosscut-section--foundational');

  var selectedFamilies = new Set();
  var selectedCrosscutGroups = new Set();

  function syncIdleState() {
    var idle = selectedFamilies.size === 0;
    surface.classList.toggle('foundry-skill-filter-idle', idle);
    surface.classList.toggle('foundry-skill-filter-active', !idle);
  }

  /* Board rows: show all when no filter; show matching family only when filter active */
  function rowVisible(row) {
    if (selectedFamilies.size === 0) return true;
    var family = row.getAttribute('data-family');
    return Boolean(family && selectedFamilies.has(family));
  }

  function otherVisible() {
    return selectedFamilies.size === 0 || selectedFamilies.has('other');
  }

  function updateCrosscutRowSkills(row) {
    var group = row.getAttribute('data-crosscut-group');
    var skills = row.querySelector('.aad-delivery-crosscut-skills');
    var expanded = Boolean(group && selectedCrosscutGroups.has(group));
    if (skills) {
      skills.classList.toggle('is-skills-visible', expanded);
      skills.classList.toggle('aad-delivery-crosscut-skills--collapsed', !expanded);
    }
    var toggle = row.querySelector('.aad-crosscut-row-toggle');
    if (toggle) {
      toggle.classList.toggle('is-selected', expanded);
      toggle.setAttribute('aria-pressed', expanded ? 'true' : 'false');
    }
  }

  /* Supporting section: same filter as board — show only selected family's row */
  function crosscutRowVisible(row) {
    if (selectedFamilies.size === 0) return true;
    var family = row.getAttribute('data-family');
    return Boolean(family && selectedFamilies.has(family));
  }

  function updateCrosscutSections() {
    var showSupporting = skillsExpanded;
    var showFoundations = skillsExpanded && otherVisible();

    crosscutPracticeRows.forEach(function (row) {
      var vis = skillsExpanded && crosscutRowVisible(row);
      row.classList.toggle('is-filter-visible', vis);
      if (vis) updateCrosscutRowSkills(row);
    });
    if (supportingSection) {
      supportingSection.classList.toggle('is-filter-visible', showSupporting);
      supportingSection.hidden = !showSupporting;
    }

    crosscutOtherRows.forEach(function (row) {
      var vis = showFoundations;
      row.classList.toggle('is-filter-visible', vis);
      if (vis) updateCrosscutRowSkills(row);
    });
    if (foundationalSection) {
      foundationalSection.classList.toggle('is-filter-visible', showFoundations);
      foundationalSection.hidden = !showFoundations;
    }

    stageSkillRows.forEach(function (row) {
      row.classList.toggle('is-filter-visible', skillsExpanded && otherVisible());
    });
  }

  function toggleCrosscutGroup(btn) {
    var group = btn.getAttribute('data-crosscut-group');
    if (!group) return;
    enableRowAnimations();
    if (selectedCrosscutGroups.has(group)) {
      selectedCrosscutGroups.delete(group);
    } else {
      selectedCrosscutGroups.add(group);
    }
    saveCrosscutPref(Array.from(selectedCrosscutGroups));
    updateCrosscutSections();
  }

  function setSkillsExpanded(expanded, source) {
    skillsExpanded = expanded;
    surface.classList.toggle('foundry-skills-collapsed', !expanded);
    surface.classList.toggle('foundry-skills-expanded', expanded);
    if (skillsToggle) {
      skillsToggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
      skillsToggle.classList.toggle('is-expanded', expanded);
      skillsToggle.setAttribute('aria-label',
        expanded ? 'Collapse practice skills across columns' : 'Expand practice skills across columns');
    }
    if (source === 'user') saveSkillsExpandedPref(expanded);
    updateCrosscutSections();
  }

  function applyFilter() {
    rows.forEach(function (row) {
      row.classList.toggle('is-filter-visible', rowVisible(row));
    });
    /* Family buttons are ALWAYS visible — never hide them */
    saveFilter(Array.from(selectedFamilies));
    updateCrosscutSections();
    syncIdleState();
  }

  function enableRowAnimations() {
    surface.classList.add('foundry-skill-nav-animated');
  }

  function setFamilySelected(btn, selected) {
    var family = btn.getAttribute('data-family');
    if (!family) return;
    if (selected) {
      selectedFamilies.add(family);
      btn.classList.add('is-selected');
      btn.setAttribute('aria-pressed', 'true');
    } else {
      selectedFamilies.delete(family);
      btn.classList.remove('is-selected');
      btn.setAttribute('aria-pressed', 'false');
    }
  }

  function toggleFamily(btn) {
    var family = btn.getAttribute('data-family');
    if (!family) return;
    enableRowAnimations();
    var nowSelected = !selectedFamilies.has(family);
    setFamilySelected(btn, nowSelected);
    /* auto-expand/collapse the matching crosscut group */
    if (nowSelected) {
      selectedCrosscutGroups.add(family);
    } else {
      selectedCrosscutGroups.delete(family);
    }
    saveCrosscutPref(Array.from(selectedCrosscutGroups));
    applyFilter();
  }

  function applyStageHighlight(stageId) {
    if (!stageId) return;
    var pageName = pageBasename();
    surface.querySelectorAll('.kb-ticket.aad-skill[data-stage]').forEach(function (el) {
      if (el.classList.contains('foundry-family-toggle')) return;
      var skillHref = (el.getAttribute('data-skill-href') || el.getAttribute('href') || '').split('?')[0];
      var onPage = skillHref === pageName;
      var inStage = el.getAttribute('data-stage') === stageId;
      el.classList.toggle('kb-ticket--current', onPage && inStage);
      if (onPage && inStage) el.setAttribute('aria-current', 'page');
      else el.removeAttribute('aria-current');
    });
    colHeads.forEach(function (head) {
      head.classList.toggle('kb-col-head--current', head.getAttribute('data-stage') === stageId);
    });
  }

  window.__foundryApplyStage = applyStageHighlight;
  window.__foundrySetSkillsExpanded = setSkillsExpanded;

  crosscutToggles.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      toggleCrosscutGroup(btn);
    });
  });

  familyButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      toggleFamily(btn);
    });
  });

  if (skillsToggle) {
    skillsToggle.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      enableRowAnimations();
      setSkillsExpanded(!skillsExpanded, 'user');
    });
  }

  /* ── Initialise state ── */
  var urlStage = stageFromUrl();
  var activeStage = urlStage || surface.getAttribute('data-initial-stage') || '';

  var saved = readSavedFilter();
  if (saved && saved.families.length) {
    saved.families.forEach(function (family) {
      familyButtons.forEach(function (btn) {
        if (btn.getAttribute('data-family') === family) setFamilySelected(btn, true);
      });
      selectedCrosscutGroups.add(family);
    });
  }

  var initialFamily = surface.getAttribute('data-initial-family');
  if (initialFamily) {
    familyButtons.forEach(function (btn) {
      if (btn.getAttribute('data-family') === initialFamily) setFamilySelected(btn, true);
    });
    selectedCrosscutGroups.add(initialFamily);
  }

  readCrosscutPref().forEach(function (group) { selectedCrosscutGroups.add(group); });

  applyFilter();
  setSkillsExpanded(readSkillsExpandedPref(), 'restore');
  applyStageHighlight(activeStage);

  window.addEventListener('popstate', function () {
    applyStageHighlight(stageFromUrl() || surface.getAttribute('data-initial-stage') || '');
  });

  window.requestAnimationFrame(function () {
    surface.classList.remove('foundry-skill-nav-settling');
  });
})();
