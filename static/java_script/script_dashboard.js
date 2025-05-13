document.addEventListener('DOMContentLoaded', function() {
  const anElements = document.querySelectorAll('.an');
  const semestruElements = document.querySelectorAll('.semestru');
  const tbodyElements = document.querySelectorAll('.dashboard_table tbody');

const materii = {
  'cibernetică economică': {
    '1-1': [
      'economie', 'algebră', 'bazele statisticii', 'bazele cercetărilor operaționale', 
      'bazele tehnologiei informației', 'bazele programării calculatoarelor', 
      'limba engleză și comunicare de specialitate 1', 'educație fizică și sport'
    ],
    '1-2': [
      'analiză matematică', 'statistică', 'algoritmi și tehnici de programare', 
      'sisteme de operare', 'bazele ciberneticii economice', 'marketing', 'contabilitate', 
      'educație fizică și sport'
    ],
    '2-1': [
      'programare orientată obiect', 'baze de date', 'statistică macroeconomică',
      'probabilități și statistică matematică', 'microeconomie cantitativă',
      'management', 'finanțe', 'educație fizică și sport'
    ],
    '2-2': [
      'analiza și diagnoza sistemelor economice', 'macroeconomie cantitativă',
      'teoria deciziei', 'simularea proceselor economice', 'econometrie',
      'microeconomie managerială', 'practică de specialitate'
    ],
    '3-1': [
      'cibernetica sistemelor economice', 'cercetări operaționale',
      'economia și gestiunea riscului', 'sisteme suport de decizie', 'analiza datelor',
      'dinamica sistemelor economice', 'sondaje și anchete statistice', 'demografie',
      'tehnologii web', 'multimedia', 'sgbd oracle', 'robotică',
      'modelare stochastică în domeniul economic'
    ],
    '3-2': [
      'sociologie', 'serii de timp', 'sisteme informaționale pentru conducere',
      'pachete software', 'teoria jocurilor', 'inteligență computațională în economie',
      'dreptul afacerilor', 'drept', 'pregătire lucrare licență'
    ]
  },
  'informatică economică': {
    '1-1': [
      'economie', 'algebră', 'bazele statisticii', 'bazele cercetărilor operaționale',
      'bazele tehnologiei informației', 'bazele programării calculatoarelor',
      'limba engleză și comunicare de specialitate 1', 'educație fizică și sport'
    ],
    '1-2': [
      'analiză matematică', 'statistică', 'algoritmi și tehnici de programare',
      'sisteme de operare', 'bazele ciberneticii economice', 'marketing', 'contabilitate',
      'educație fizică și sport'
    ],
    '2-1': [
      'programare orientată obiect', 'baze de date', 'statistică macroeconomică',
      'probabilități și statistică matematică', 'microeconomie cantitativă',
      'management', 'finanțe', 'educație fizică și sport'
    ],
    '2-2': [
      'programarea aplicațiilor windows', 'macroeconomie cantitativă',
      'programare evolutivă și algoritmi genetici', 'structuri de date',
      'programare multiparadigmă - java', 'sgbd oracle', 'practică de specialitate'
    ],
    '3-1': [
      'econometrie', 'analiza și proiectarea sistemelor informatice',
      'dispozitive și aplicații mobile', 'multimedia',
      'dezvoltare software pentru analiza datelor', 'tehnologii web'
    ],
    '3-2': [
      'sociologie', 'serii de timp', 'rețele de calculatoare',
      'pachete software', 'sisteme informaționale economice',
      'calitate și testare software'
    ]
  },
  'statistică și previziune economică': {
    '1-1': [
      'economie', 'algebră', 'bazele statisticii', 'bazele cercetărilor operaționale',
      'bazele tehnologiei informației', 'bazele programării calculatoarelor', 'educație fizică și sport'
    ],
    '1-2': [
      'analiză matematică', 'statistică', 'algoritmi și tehnici de programare',
      'sisteme de operare', 'bazele ciberneticii economice', 'educație fizică și sport'
    ],
    '2-1': [
      'programare orientată obiect', 'baze de date', 'statistică macroeconomică',
      'probabilități și statistică matematică', 'microeconomie cantitativă', 'management',
      'finanțe', 'educație fizică și sport'
    ],
    '2-2': [
      'pachete software', 'statistică neparametrică', 'econometrie',
      'statistică spațială', 'testarea ipotezelor statistice',
      'macroeconomie cantitativă', 'practică de specialitate'
    ],
    '3-1': [
      'modelarea și vizualizarea geospațială a datelor statistice',
      'controlul statistic al calității', 'analiză statistică multidimensională',
      'sondaje și anchete statistice', 'demografie', 'teoria jocurilor',
      'cercetări operaționale', 'dinamica sistemelor economice',
      'programarea aplicațiilor Windows', 'tehnologii web', 'sgbd oracle',
      'robotică', 'modelare stochastică în domeniul economic'
    ],
    '3-2': [
      'previziune economică', 'statistica piețelor financiare', 'serii de timp',
      'statistică microeconomică', 'sociologie',
      'proiectarea sistemelor informatice în statistică', 'dreptul afacerilor', 'drept'
    ]
  }
};

const optiuniOptionale = {
  '2-1': {
    optiuni: [
      'construcţie şi depanare pc', 'modele regionale de economie', 'istoria economiei',
      'comunicare în limba engleză 1', 'comunicare în limba franceză 1',
      'comunicare în limba rusă 1', 'comunicare în limba spaniolă 1',
      'comunicare în limba italiană 1', 'comunicare în limba germană 1',
      'comunicare în limba turcă 1', 'comunicare în limba japoneză 1',
      'comunicare în limba chineză 1'
    ],
    numar: 2
  },
  '2-2': {
    optiuni: [
      'doctrine economice', 'competiție și competitivitate', 'comunicare în limba engleză 2',
      'comunicare în limba germană 2', 'comunicare în limba turcă 2',
      'comunicare în limba japoneză 2', 'comunicare în limba chineză 2',
      'comunicare în limba franceză 2', 'comunicare în limba rusă 2',
      'comunicare în limba spaniolă 2', 'comunicare în limba italiană 2',
      'managementul riscului în afaceri internaționale', 'antreprenoriat în comerț, turism și servicii',
      'finanțe corporative', 'negocieri internaționale', 'managementul relațiilor cu clienții',
      'etică şi integritate academică', 'economia informației digitale cu aplicații în afaceri',
      'dezvoltare durabilă', 'analiza economico-financiară',
      'tehnici de scriere academică și învățare eficientă'
    ],
    numar: 2
  }
};

  function validateNota(cell) {
    let value = cell.innerText.trim();
    if (!/^\d+$/.test(value) || value < 1 || value > 10) {
      alert('nota trebuie să fie între 1 și 10.');
      cell.innerText = '';
    }
  }

  function validateOptionale() {
    const selects = document.querySelectorAll('select');
    if (selects.length > 1) {
      const [select1, select2] = selects;

      const val1 = select1.value;
      const val2 = select2.value;

      if (val1 && val2 && val1 === val2) {
        alert('nu poți alege aceeași materie opțională de două ori.');
        select2.value = '';
      }

      if (!val1 && !val2) {
        alert('trebuie să alegi cel puțin o materie opțională.');
      }
    }
  }

function getNextSemester(an, semestru) {
    let nextAn = parseInt(an);
    let nextSemestru = parseInt(semestru);
    
    if (nextSemestru === 1) {
        nextSemestru = 2;
    } else {
        nextSemestru = 1;
        nextAn += 1;
    }

    const cheie = `${nextAn}-${nextSemestru}`;
    
    if (!materii[specializare] || !materii[specializare][cheie]) {
        return null;
    }
    
    return { an: nextAn, semestru: nextSemestru };
}

function updateTable(tbody, listaMaterii, optionalData) {
    tbody.innerHTML = '';

    if (listaMaterii) {
        listaMaterii.forEach(materie => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${materie}</td>
                <td contenteditable="true" class="nota"></td>
            `;
            tbody.appendChild(tr);
        });

        if (optionalData) {
            for (let i = 0; i < optionalData.numar; i++) {
                const optionalRow = document.createElement('tr');
                const selectHTML = optionalData.optiuni.map(opt => `<option value="${opt}">${opt}</option>`).join('');
                optionalRow.innerHTML = `
                    <td>
                        <select>
                            <option disabled selected>alege materie opțională...</option>
                            ${selectHTML}
                        </select>
                    </td>
                    <td contenteditable="true" class="nota"></td>
                `;
                tbody.appendChild(optionalRow);
            }

            tbody.querySelectorAll('select').forEach(select => {
                select.addEventListener('change', validateOptionale);
            });
        }

        tbody.querySelectorAll('.nota').forEach(cell => {
            cell.addEventListener('blur', () => validateNota(cell));
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="2" style="text-align:center;">nu există date pentru acest an/semestru</td></tr>';
    }
}

function updateMaterii() {
    const an = document.querySelectorAll('.an')[0].textContent.trim();
    const semestru = document.querySelectorAll('.semestru')[0].textContent.trim();
    const cheie = `${an}-${semestru}`;
    
    const listaMaterii = materii[specializare] ? materii[specializare][cheie] : null;
    const optionalData = optiuniOptionale[cheie] || null;

    const tbodyTop = tbodyElements[0];
    updateTable(tbodyTop, listaMaterii, optionalData);

    const nextSemester = getNextSemester(an, semestru);
    const tbodyBottom = tbodyElements[1];
    const headersBottom = document.querySelectorAll('.dashboard_headers')[1];
    
    if (nextSemester) {
        const nextCheie = `${nextSemester.an}-${nextSemester.semestru}`;
        const nextListaMaterii = materii[specializare] ? materii[specializare][nextCheie] : null;
        const nextOptionalData = optiuniOptionale[nextCheie] || null;
        
        headersBottom.querySelector('.an').textContent = nextSemester.an;
        headersBottom.querySelector('.semestru').textContent = nextSemester.semestru;
        
        updateTable(tbodyBottom, nextListaMaterii, nextOptionalData);

        headersBottom.querySelector('.an').setAttribute('contenteditable', 'false');
        headersBottom.querySelector('.semestru').setAttribute('contenteditable', 'false');
    } else {
        headersBottom.querySelector('.an').textContent = '';
        headersBottom.querySelector('.semestru').textContent = '';
        tbodyBottom.innerHTML = '<tr><td colspan="2" style="text-align:center;">nu există un următor semestru</td></tr>';
    }
}

  document.querySelectorAll('.an')[0].addEventListener('blur', function() {
    let value = this.innerText.trim();
    if (!/^\d+$/.test(value) || value < 1 || value > 3) {
      alert('anul trebuie să fie între 1 și 3.');
      this.innerText = '1';
    }
    updateMaterii();
  });

  document.querySelectorAll('.semestru')[0].addEventListener('blur', function() {
    let value = this.innerText.trim();
    if (!/^\d+$/.test(value) || value < 1 || value > 2) {
      alert('semestrul trebuie să fie între 1 și 2.');
      this.innerText = '1';
    }
    updateMaterii();
  });

  updateMaterii();
});