document.addEventListener('DOMContentLoaded', () => {
  const bezugOptions = ['--', 'Lager', 'Werk 19', 'Werk 10', 'Extern', 'Hausteil'];
  let selectedBezug = '--'; 

  // Funktion zum Erstellen des Dropdown-Menüs
  const createBezugDropdown = () => {
    const select = document.createElement('select');
    bezugOptions.forEach(option => {
      const opt = document.createElement('option');
      opt.value = option;
      opt.innerHTML = option;
      if (option === selectedBezug) {
        opt.selected = true;
      }
      select.appendChild(opt);
    });
    return select;
  };

  const calculateLiefertermin = (bezug) => {
    let tageHinzufuegen = 0;
    if (bezug === 'Lager') {
      tageHinzufuegen = 1;
    } else if (['Werk 19', 'Extern'].includes(bezug)) {
      tageHinzufuegen = 2;
    } else if (['Hausteil'].includes(bezug)) {
      tageHinzufuegen = 14;
    } else if (['Werk 10'].includes(bezug)){
      tageHinzufuegen = 3;
    }

    const heute = new Date();
    heute.setDate(heute.getDate() + tageHinzufuegen);

    // Formatieren als 'DD-MM-YYYY'
    return heute.getDate().toString().padStart(2, '0') + '-' +
      (heute.getMonth() + 1).toString().padStart(2, '0') + '-' +
      heute.getFullYear();
  };

  const getRowBackgroundColor = (bezugValue) => {
    switch (bezugValue) {
      case 'Lager': return '#b4ff8f'; // Example color for 'Lager'
      case 'Werk 19': return '#ffff8f';
      case 'Werk 10': return '#ffc58f';
      case 'Hausteil': return '#ff8f8f';
      case 'Extern': return '#f48fff';
      default: return '#ffffff'; // Default (no background color)
    }
  };


  const hot = new Handsontable(document.getElementById('infoTable'), {
    data: [],
    colHeaders: [
      'Teilenummer',
      'Bezeichnung',
      'Menge',
      'Bezug',
      'Liefertermin'
    ],
    columns: [
      { data: 'teilenummer' },
      { data: 'bezeichnung' },
      { data: 'menge', type: 'numeric' },
      { data: 'bezug', type: 'dropdown', source: bezugOptions },
      { data: 'liefertermin', type: 'date', dateFormat: 'DD-MM-YYYY' }
    ],
    cells: function (row, col) {
      var cellProperties = {};
      var bezugValue = this.instance.getDataAtCell(row, 3); // Holt den Wert aus der 'bezug' Spalte
      cellProperties.renderer = function (instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.background = getRowBackgroundColor(bezugValue); // Setzt den Hintergrund basierend auf dem 'bezug' Wert
      };
      return cellProperties;
    },
    afterGetColHeader: function (col, TH) {
      if (col === 3) {
        const select = createBezugDropdown();
        select.onchange = function () {
          selectedBezug = this.value;
          for (let i = 0; i < hot.countRows(); i++) {
            hot.setDataAtCell(i, 3, selectedBezug);
          }
        };
        while (TH.firstChild) {
          TH.removeChild(TH.firstChild);
        }
        TH.appendChild(select);
      }
    },

    dropdownMenu: true,
    contextMenu: true,
    minSpareRows: 1,
    minRow: 8,
    allowRemoveRow: true,
    licenseKey: 'non-commercial-and-evaluation'
  });


  window.myHandsontable = hot;

  hot.addHook('afterChange', (changes, source) => {
    if (changes) {
      let bezugChanged = false;
      changes.forEach(([row, prop, oldValue, newValue]) => {
        if (prop === 'bezug') {
          const neuesLiefertermin = calculateLiefertermin(newValue);
          hot.setDataAtRowProp(row, 'liefertermin', neuesLiefertermin);
          bezugChanged = true;
        }
      });
      if (bezugChanged) {
        hot.render(); // Führt ein Re-Rendering der Tabelle aus
      }
    }
  });
});
