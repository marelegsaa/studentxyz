document.addEventListener('DOMContentLoaded', function() {
    const yearSelect = document.getElementById('yearSelect');
    const semesterSelect = document.getElementById('semesterSelect');
    const gradesTableBody = document.getElementById('gradesTableBody');
    const currentPeriodTitle = document.getElementById('currentPeriodTitle');
    const predictionSection = document.getElementById('predictionSection');
    const generatePredictionsBtn = document.getElementById('generatePredictions');
    const predictionResults = document.getElementById('predictionResults');
    const predictionTableBody = document.getElementById('predictionTableBody');

    yearSelect.value = String(anCurent);
    semesterSelect.value = String(semestruCurent);

    let currentPredictions = null;

    function isPhysicalEducation(materie) {
        return materie.toLowerCase().includes('educație fizică') || 
               materie.toLowerCase().includes('educatie fizica') ||
               materie.toLowerCase().includes('educație fizică și sport') ||
               materie.toLowerCase().includes('educatie fizica si sport');
    }

    const materii = {
        'cibernetică economică': {
            '1-1': ['economie', 'algebră', 'bazele statisticii', 'bazele cercetărilor operaționale', 
                    'bazele tehnologiei informației', 'bazele programării calculatoarelor', 
                    'limba engleză și comunicare de specialitate 1', 'educație fizică și sport'],
            '1-2': ['analiză matematică', 'statistică', 'algoritmi și tehnici de programare', 
                    'sisteme de operare', 'bazele ciberneticii economice', 'marketing', 'contabilitate', 
                    'educație fizică și sport'],
            '2-1': ['programare orientată obiect', 'baze de date', 'statistică macroeconomică',
                    'probabilități și statistică matematică', 'microeconomie cantitativă',
                    'management', 'finanțe', 'educație fizică și sport'],
            '2-2': ['analiza și diagnoza sistemelor economice', 'macroeconomie cantitativă',
                    'teoria deciziei', 'simularea proceselor economice', 'econometrie',
                    'microeconomie managerială', 'practică de specialitate'],
            '3-1': ['cibernetica sistemelor economice', 'cercetări operaționale',
                    'economia și gestiunea riscului', 'sisteme suport de decizie', 'analiza datelor',
                    'dinamica sistemelor economice', 'sondaje și anchete statistice', 'demografie',
                    'tehnologii web', 'multimedia', 'sgbd oracle', 'robotică',
                    'modelare stochastică în domeniul economic'],
            '3-2': ['sociologie', 'serii de timp', 'sisteme informaționale pentru conducere',
                    'pachete software', 'teoria jocurilor', 'inteligență computațională în economie',
                    'dreptul afacerilor', 'drept', 'pregătire lucrare licență']
        },
        'informatică economică': {
            '1-1': ['economie', 'algebră', 'bazele statisticii', 'bazele cercetărilor operaționale',
                    'bazele tehnologiei informației', 'bazele programării calculatoarelor',
                    'limba engleză și comunicare de specialitate 1', 'educație fizică și sport'],
            '1-2': ['analiză matematică', 'statistică', 'algoritmi și tehnici de programare',
                    'sisteme de operare', 'bazele ciberneticii economice', 'marketing', 'contabilitate',
                    'educație fizică și sport'],
            '2-1': ['programare orientată obiect', 'baze de date', 'statistică macroeconomică',
                    'probabilități și statistică matematică', 'microeconomie cantitativă',
                    'management', 'finanțe', 'educație fizică și sport'],
            '2-2': ['programarea aplicațiilor windows', 'macroeconomie cantitativă',
                    'programare evolutivă și algoritmi genetici', 'structuri de date',
                    'programare multiparadigmă - java', 'sgbd oracle', 'practică de specialitate'],
            '3-1': ['econometrie', 'analiza și proiectarea sistemelor informatice',
                    'dispozitive și aplicații mobile', 'multimedia',
                    'dezvoltare software pentru analiza datelor', 'tehnologii web'],
            '3-2': ['sociologie', 'serii de timp', 'rețele de calculatoare',
                    'pachete software', 'sisteme informaționale economice',
                    'calitate și testare software', 'dreptul afacerilor', 
                    'drept', 'pregătire lucrare licență']
        },
        'statistică și previziune economică': {
            '1-1': ['economie', 'algebră', 'bazele statisticii', 'bazele cercetărilor operaționale',
                    'bazele tehnologiei informației', 'bazele programării calculatoarelor', 'educație fizică și sport'],
            '1-2': ['analiză matematică', 'statistică', 'algoritmi și tehnici de programare',
                    'sisteme de operare', 'bazele ciberneticii economice', 'educație fizică și sport'],
            '2-1': ['programare orientată obiect', 'baze de date', 'statistică macroeconomică',
                    'probabilități și statistică matematică', 'microeconomie cantitativă', 'management',
                    'finanțe', 'educație fizică și sport'],
            '2-2': ['pachete software', 'statistică neparametrică', 'econometrie',
                    'statistică spațială', 'testarea ipotezelor statistice',
                    'macroeconomie cantitativă', 'practică de specialitate'],
            '3-1': ['modelarea și vizualizarea geospațială a datelor statistice',
                    'controlul statistic al calității', 'analiză statistică multidimensională',
                    'sondaje și anchete statistice', 'demografie', 'teoria jocurilor',
                    'cercetări operaționale', 'dinamica sistemelor economice',
                    'programarea aplicațiilor Windows', 'tehnologii web', 'sgbd oracle',
                    'robotică', 'modelare stochastică în domeniul economic'],
            '3-2': ['previziune economică', 'statistica piețelor financiare', 'serii de timp',
                    'statistică microeconomică', 'sociologie',
                    'proiectarea sistemelor informatice în statistică', 'dreptul afacerilor', 'drept']
        }
    };

    const credite = {
        'cibernetică economică': {
            '1-1': {'economie': 5, 'algebră': 5, 'bazele statisticii': 5, 'bazele cercetărilor operaționale': 4,
                    'bazele tehnologiei informației': 6, 'bazele programării calculatoarelor': 3,
                    'limba engleză și comunicare de specialitate 1': 2, 'educație fizică și sport': 1},
            '1-2': {'analiză matematică': 5, 'statistică': 5, 'algoritmi și tehnici de programare': 4,
                    'sisteme de operare': 4, 'bazele ciberneticii economice': 4, 'marketing': 4,
                    'contabilitate': 4, 'educație fizică și sport': 1},
            '2-1': {'programare orientată obiect': 5, 'baze de date': 5, 'statistică macroeconomică': 4,
                    'probabilități și statistică matematică': 4, 'microeconomie cantitativă': 4,
                    'management': 4, 'finanțe': 4, 'educație fizică și sport': 1},
            '2-2': {'analiza și diagnoza sistemelor economice': 4, 'macroeconomie cantitativă': 4,
                    'teoria deciziei': 4, 'simularea proceselor economice': 4, 'econometrie': 4,
                    'microeconomie managerială': 4, 'practică de specialitate': 3},
            '3-1': {'cibernetica sistemelor economice': 5, 'cercetări operaționale': 5,
                    'economia și gestiunea riscului': 4, 'sisteme suport de decizie': 4, 'analiza datelor': 4,
                    'dinamica sistemelor economice': 4, 'sondaje și anchete statistice': 4, 'demografie': 4,
                    'tehnologii web': 4, 'multimedia': 4, 'sgbd oracle': 4, 'robotică': 4,
                    'modelare stochastică în domeniul economic': 4},
            '3-2': {'sociologie': 2, 'serii de timp': 4, 'sisteme informaționale pentru conducere': 5,
                    'pachete software': 5, 'teoria jocurilor': 5, 'inteligență computațională în economie': 5,
                    'dreptul afacerilor': 4, 'drept': 4, 'pregătire lucrare licență': 0}
        },
        'informatică economică': {
            '1-1': {'economie': 5, 'algebră': 5, 'bazele statisticii': 5, 'bazele cercetărilor operaționale': 4,
                    'bazele tehnologiei informației': 6, 'bazele programării calculatoarelor': 3,
                    'limba engleză și comunicare de specialitate 1': 2, 'educație fizică și sport': 1},
            '1-2': {'analiză matematică': 5, 'statistică': 5, 'algoritmi și tehnici de programare': 4,
                    'sisteme de operare': 4, 'bazele ciberneticii economice': 4, 'marketing': 4,
                    'contabilitate': 4, 'educație fizică și sport': 1},
            '2-1': {'programare orientată obiect': 5, 'baze de date': 5, 'statistică macroeconomică': 4,
                    'probabilități și statistică matematică': 4, 'microeconomie cantitativă': 4,
                    'management': 4, 'finanțe': 4, 'educație fizică și sport': 1},
            '2-2': {'programarea aplicațiilor windows': 4, 'macroeconomie cantitativă': 4,
                    'programare evolutivă și algoritmi genetici': 4, 'structuri de date': 4,
                    'programare multiparadigmă - java': 4, 'sgbd oracle': 4, 'practică de specialitate': 3},
            '3-1': {'econometrie': 4, 'analiza și proiectarea sistemelor informatice': 5,
                    'dispozitive și aplicații mobile': 5, 'multimedia': 4,
                    'dezvoltare software pentru analiza datelor': 4, 'tehnologii web': 4,
                    'demografie': 4, 'sondaje și anchete statistice': 4, 'robotică': 4,
                    'modelare stochastică în domeniul economic': 4},
            '3-2': {'sociologie': 2, 'serii de timp': 4, 'rețele de calculatoare': 5,
                    'pachete software': 5, 'sisteme informaționale economice': 5,
                    'calitate și testare software': 5, 'dreptul afacerilor': 4, 'drept': 4,
                    'pregătire lucrare licență': 0}
        },
        'statistică și previziune economică': {
            '1-1': {'economie': 5, 'algebră': 5, 'bazele statisticii': 5, 'bazele cercetărilor operaționale': 4,
                    'bazele tehnologiei informației': 6, 'bazele programării calculatoarelor': 3,
                    'limba engleză și comunicare de specialitate 1': 2, 'educație fizică și sport': 1},
            '1-2': {'analiză matematică': 5, 'statistică': 5, 'algoritmi și tehnici de programare': 4,
                    'sisteme de operare': 4, 'bazele ciberneticii economice': 4, 'marketing': 4,
                    'contabilitate': 4, 'educație fizică și sport': 1},
            '2-1': {'programare orientată obiect': 5, 'baze de date': 5, 'statistică macroeconomică': 4,
                    'probabilități și statistică matematică': 4, 'microeconomie cantitativă': 4,
                    'management': 4, 'finanțe': 4, 'educație fizică și sport': 1},
            '2-2': {'pachete software': 4, 'statistică neparametrică': 4, 'econometrie': 4,
                    'statistică spațială': 4, 'testarea ipotezelor statistice': 4,
                    'macroeconomie cantitativă': 4, 'practică de specialitate': 3},
            '3-1': {'modelarea și vizualizarea geospațială a datelor statistice': 4,
                    'controlul statistic al calității': 5, 'analiză statistică multidimensională': 5,
                    'sondaje și anchete statistice': 4, 'demografie': 4, 'teoria jocurilor': 4,
                    'cercetări operaționale': 4, 'dinamica sistemelor economice': 4,
                    'programarea aplicațiilor windows': 4, 'tehnologii web': 4, 'sgbd oracle': 4,
                    'robotică': 4, 'modelare stochastică în domeniul economic': 4},
            '3-2': {'previziune economică': 5, 'statistica piețelor financiare': 5, 'serii de timp': 5,
                    'statistică microeconomică': 4, 'sociologie': 2,
                    'proiectarea sistemelor informatice în statistică': 5, 'dreptul afacerilor': 3,
                    'drept': 3, 'pregătire lucrare licență': 0}
        }
    };

    const crediteOptionale = {
        '2-1': {
            'construcție și depanare pc': 4,
            'modele regionale de economie': 4,
            'istoria economiei': 4,
            'comunicare în limba engleză 1': 4,
            'comunicare în limba franceză 1': 4,
            'comunicare în limba rusă 1': 4,
            'comunicare în limba spaniolă 1': 4,
            'comunicare în limba italiană 1': 4,
            'comunicare în limba germană 1': 4,
            'comunicare în limba turcă 1': 4,
            'comunicare în limba japoneză 1': 4,
            'comunicare în limba chineză 1': 4
        },
        '2-2': {
            'managementul riscului în afaceri internaționale': 3,
            'antreprenoriat în comerț, turism și servicii': 3,
            'finanțe corporative': 3,
            'negocieri internaționale': 3,
            'managementul relațiilor cu clienții': 3,
            'etică și integritate academică': 3,
            'economia informației digitale cu aplicații în afaceri': 3,
            'dezvoltare durabilă': 3,
            'analiza economico-financiară': 3,
            'tehnici de scriere academică și învățare eficientă': 3,
            
            'doctrine economice': 4,
            'competiție și competitivitate': 4,
            'comunicare în limba engleză 2': 4,
            'comunicare în limba germană 2': 4,
            'comunicare în limba turcă 2': 4,
            'comunicare în limba japoneză 2': 4,
            'comunicare în limba chineză 2': 4,
            'comunicare în limba franceză 2': 4,
            'comunicare în limba rusă 2': 4,
            'comunicare în limba spaniolă 2': 4,
            'comunicare în limba italiană 2': 4
        }
    };
    
    const optiuniOptionale = {
        '2-1': {
            optiuni: ['construcție și depanare pc', 'modele regionale de economie', 'istoria economiei',
                     'comunicare în limba engleză 1', 'comunicare în limba franceză 1',
                     'comunicare în limba rusă 1', 'comunicare în limba spaniolă 1',
                     'comunicare în limba italiană 1', 'comunicare în limba germană 1',
                     'comunicare în limba turcă 1', 'comunicare în limba japoneză 1',
                     'comunicare în limba chineză 1'],
            numar: 2
        },
        '2-2': {
            optiuni: ['doctrine economice', 'competiție și competitivitate', 'comunicare în limba engleză 2',
                     'comunicare în limba germană 2', 'comunicare în limba turcă 2',
                     'comunicare în limba japoneză 2', 'comunicare în limba chineză 2',
                     'comunicare în limba franceză 2', 'comunicare în limba rusă 2',
                     'comunicare în limba spaniolă 2', 'comunicare în limba italiană 2',
                     'managementul riscului în afaceri internaționale', 'antreprenoriat în comerț, turism și servicii',
                     'finanțe corporative', 'negocieri internaționale', 'managementul relațiilor cu clienții',
                     'etică și integritate academică', 'economia informației digitale cu aplicații în afaceri',
                     'dezvoltare durabilă', 'analiza economico-financiară',
                     'tehnici de scriere academică și învățare eficientă'],
            numar: 2
        }
    };

    let optionaleSelectate = {};

    function getCreditePentruMaterie(materie, cheie, specializare) {
        if (credite[specializare] && credite[specializare][cheie] && credite[specializare][cheie][materie]) {
            return credite[specializare][cheie][materie];
        }
        
        if (crediteOptionale[cheie] && crediteOptionale[cheie][materie]) {
            return crediteOptionale[cheie][materie];
        }
        
        if (optiuniOptionale[cheie] && optiuniOptionale[cheie].optiuni.includes(materie)) {
            return 4;
        }
        
        return isPhysicalEducation(materie) ? 1 : 3;
    }
    
    function showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    function saveDashboardPosition(year, semester) {
        fetch('/save_dashboard_position', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                year: year,
                semester: semester
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Dashboard position saved:', year, semester);
            }
        })
        .catch(error => {
            console.error('Error saving dashboard position:', error);
        });
    }

    function updateAverageDisplay(year, semester) {
        fetch(`/api/get_averages?year=${year}&semester=${semester}`)
        .then(response => response.json())
        .then(data => {
            const semesterAvg = data.semester_average ? data.semester_average.toFixed(2) : '-';
            const overallAvg = data.overall_average ? data.overall_average.toFixed(2) : '-';

            document.getElementById('avgGrade').textContent = semesterAvg;

            const avgElement = document.getElementById('avgGrade');
            avgElement.setAttribute('title', `Media generală: ${overallAvg}`);
        })
        .catch(error => {
            console.error('Error fetching averages:', error);
            updateLocalAverage();
        });
    }

    function updateLocalAverage() {
        const an = yearSelect.value;
        const semestru = semesterSelect.value;
        const cheie = `${an}-${semestru}`;
        
        let totalCredits = 0;
        let totalWeighted = 0;
        let gradesCount = 0;
        
        if (materii[specializare] && materii[specializare][cheie]) {
            materii[specializare][cheie].forEach(materie => {
                const gradeKey = `${an}-${semestru}-${materie}`;
                const gradeValue = note[gradeKey];
                
                if (gradeValue) {
                    const creditValue = getCreditePentruMaterie(materie, cheie, specializare);
                    
                    if (isPhysicalEducation(materie)) {
                        if (gradeValue === 'admis' && creditValue > 0) {
                            totalCredits += creditValue;
                        }
                    } else {
                        const gradeNum = parseInt(gradeValue);
                        if (!isNaN(gradeNum) && gradeNum >= 5 && creditValue > 0) {
                            totalWeighted += gradeNum * creditValue;
                            gradesCount += creditValue;
                            totalCredits += creditValue;
                        }
                    }
                }
            });
        }
        
        const avgGrade = gradesCount > 0 ? (totalWeighted / gradesCount).toFixed(2) : '-';
        document.getElementById('avgGrade').textContent = avgGrade;
        document.getElementById('totalCredits').textContent = totalCredits;
    }

    function checkNextSemesterExists(year, semester) {
        const transitions = {
            '1-1': '1-2',
            '1-2': '2-1',
            '2-1': '2-2',
            '2-2': '3-1',
            '3-1': '3-2'
        };
        
        return transitions[`${year}-${semester}`] !== undefined;
    }

    function getGradesForCurrentSemester() {
        const an = yearSelect.value;
        const semestru = semesterSelect.value;
        const cheie = `${an}-${semestru}`;
        
        const grades = [];
        
        if (materii[specializare] && materii[specializare][cheie]) {
            materii[specializare][cheie].forEach(materie => {
                const gradeKey = `${an}-${semestru}-${materie}`;
                const gradeValue = note[gradeKey];

                if (isPhysicalEducation(materie)) {
                    if (gradeValue && ['admis', 'respins'].includes(gradeValue)) {
                        grades.push({
                            subject: materie,
                            grade: gradeValue,
                            credits: getCreditePentruMaterie(materie, cheie, specializare),
                            isPE: true
                        });
                    }
                } else if (gradeValue) {
                    const numericGrade = parseInt(gradeValue);
                    if (!isNaN(numericGrade)) {
                        grades.push({
                            subject: materie,
                            grade: numericGrade,
                            credits: getCreditePentruMaterie(materie, cheie, specializare),
                            isPE: false
                        });
                    }
                }
            });
        }
        
        return grades;
    }

    function updatePredictionSection() {
        const year = parseInt(yearSelect.value);
        const semester = parseInt(semesterSelect.value);

        if (checkNextSemesterExists(year, semester)) {
            predictionSection.classList.add('show');

            const currentGrades = getGradesForCurrentSemester();
            if (currentGrades.length > 0) {
                generatePredictionsBtn.disabled = false;
                generatePredictionsBtn.querySelector('.btn_text').textContent = 'generează predicții';
            } else {
                generatePredictionsBtn.disabled = true;
                generatePredictionsBtn.querySelector('.btn_text').textContent = 'introduceți note mai întâi';
            }

            const transitions = {
                '1-1': 'anul 1, semestrul 2',
                '1-2': 'anul 2, semestrul 1',
                '2-1': 'anul 2, semestrul 2',
                '2-2': 'anul 3, semestrul 1',
                '3-1': 'anul 3, semestrul 2'
            };
            
            const nextPeriod = transitions[`${year}-${semester}`];
            document.getElementById('predictionPeriodTitle').innerHTML = `🔮 predicții pentru ${nextPeriod}`;
        } else {
            predictionSection.classList.remove('show');
        }

        predictionResults.classList.remove('show');
        currentPredictions = null;
    }

    function getConfidenceClass(confidence) {
        if (confidence >= 0.8) return 'high';
        if (confidence >= 0.6) return 'medium';
        return 'low';
    }

    function getConfidenceText(confidence) {
        if (confidence >= 0.8) return 'mare';
        if (confidence >= 0.6) return 'medie';
        return 'mică';
    }

    function displayPredictions(predictions) {
        predictionTableBody.innerHTML = '';
        
        const year = predictions.next_year;
        const semester = predictions.next_semester;
        const nextSemesterKey = `${year}-${semester}`;
        
        let totalPredictedGrades = 0;
        let totalSubjects = 0;
        let numericalSubjects = 0; 
        
        Object.entries(predictions.predictions).forEach(([subject, predictedValue]) => {
            const tr = document.createElement('tr');
            
            const creditValue = getCreditePentruMaterie(subject, nextSemesterKey, specializare);
            const confidence = predictions.confidence;
            
            let displayValue = '';
            let confidenceDisplay = '';
            
            if (isPhysicalEducation(subject)) {
                displayValue = `<span class="predicted_pe ${predictedValue}">${predictedValue}</span>`;
                confidenceDisplay = '<span class="confidence_badge high">mare</span>';
            } else {
                displayValue = `<span class="predicted_grade">${predictedValue}</span>`;
                confidenceDisplay = `<span class="confidence_badge ${getConfidenceClass(confidence)}">${getConfidenceText(confidence)}</span>`;
                totalPredictedGrades += predictedValue;
                numericalSubjects++;
            }
            
            totalSubjects++;
            
            tr.innerHTML = `
                <td>${subject}</td>
                <td>${creditValue}</td>
                <td>${displayValue}</td>
                <td>${confidenceDisplay}</td>
            `;
            
            predictionTableBody.appendChild(tr);
        });
        
        const averagePredicted = numericalSubjects > 0 ? (totalPredictedGrades / numericalSubjects).toFixed(2) : '-';
        document.getElementById('predictedAverage').textContent = averagePredicted;
        document.getElementById('predictionConfidence').textContent = `${Math.round(predictions.confidence * 100)}%`;
        
        predictionResults.classList.add('show');
        predictionResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    generatePredictionsBtn.addEventListener('click', function() {
        const year = parseInt(yearSelect.value);
        const semester = parseInt(semesterSelect.value);
        
        this.disabled = true;
        this.querySelector('.btn_text').textContent = 'se generează...';
        this.querySelector('.btn_icon').textContent = '⏳';
        
        fetch('/api/predict_grades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                year: year,
                semester: semester
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentPredictions = data.predictions;
                displayPredictions(data.predictions);
                showToast('predicții generate cu succes!', 'success');
            } else {
                showToast(data.message || 'eroare la generarea predicțiilor', 'error');
            }
        })
        .catch(error => {
            console.error('Error generating predictions:', error);
            showToast('eroare de conexiune la generarea predicțiilor', 'error');
        })
        .finally(() => {
            this.disabled = false;
            this.querySelector('.btn_text').textContent = 'generează predicții';
            this.querySelector('.btn_icon').textContent = '✨';
        });
    });

    let availablePeriods = [];

    function checkAvailablePeriods() {
        fetch('/api/get_available_periods')
            .then(response => response.json())
            .then(data => {
                availablePeriods = data.available_periods || [];
                updateInputStates();
            })
            .catch(error => {
                console.error('Error fetching available periods:', error);
                availablePeriods = ['1-1', '1-2', '2-1', '2-2', '3-1', '3-2'];
            });
    }

    function updateInputStates() {
        const an = yearSelect.value;
        const semestru = semesterSelect.value;
        const currentPeriod = `${an}-${semestru}`;
        
        const inputs = document.querySelectorAll('.grade-input, .pe-select');

        const isPeriodAllowed = availablePeriods.includes(currentPeriod);

        inputs.forEach(input => {
            if (!isPeriodAllowed) {
                input.disabled = true;
            } else {
                const row = input.closest('tr');
                const checkbox = row.querySelector('input[type="checkbox"]');

                if (checkbox) {
                    input.disabled = !checkbox.checked;
                } else {
                    input.disabled = false;
                }
            }
        });

        const messageEl = document.getElementById('period-lock-message');
        if (!isPeriodAllowed) {
            fetch(`/api/get_missing_subjects?year=${an}&semester=${semestru}`)
                .then(response => response.json())
                .then(data => {
                    if (data.missing_subjects && data.missing_subjects.length > 0) {
                        const missingList = data.missing_subjects.slice(0, 3).join(', ');
                        const moreText = data.missing_subjects.length > 3 ? ` și altele...` : '';
                        messageEl.innerHTML = `
                            <strong>pentru a adăuga note în această perioadă, trebuie să completezi notele din ${data.required_period}</strong><br>
                            materiile lipsă: <em>${missingList}${moreText}</em>
                        `;
                    } else {
                        messageEl.textContent = `completează toate notele obligatorii din ${data.required_period}`;
                    }
                    if (messageEl) {
                        messageEl.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error fetching missing subjects:', error);
                    if (messageEl) {
                        messageEl.style.display = 'block';
                        messageEl.textContent = `completează toate notele din perioada anterioară`;
                    }
                });
        } else {
            if (messageEl) {
                messageEl.style.display = 'none';
            }
        }
    }
    
    function updateTable() {
        const an = yearSelect.value;
        const semestru = semesterSelect.value;
        const cheie = `${an}-${semestru}`;

        currentPeriodTitle.textContent = `anul ${an}, semestrul ${semestru}`;

        gradesTableBody.innerHTML = '';

        const listaMaterii = materii[specializare] ? materii[specializare][cheie] : null;
        const optionalData = optiuniOptionale[cheie] || null;
        
        let totalCredits = 0;
        let passedCount = 0;
        let failedCount = 0;
        let pendingCount = 0;
        
        if (listaMaterii) {
            listaMaterii.forEach(materie => {
                const tr = document.createElement('tr');
                
                const creditValue = getCreditePentruMaterie(materie, cheie, specializare);
                const gradeKey = `${an}-${semestru}-${materie}`;
                const gradeValue = note[gradeKey] || '';
                
                let status = '<span class="status_badge pending">în așteptare</span>';
                let gradeInput = '';
                
                if (isPhysicalEducation(materie)) {
                    gradeInput = `
                        <select class="pe-select" 
                                data-key="${gradeKey}"
                                onchange="updateGrade(this)">
                            <option value="">selectează</option>
                            <option value="admis" ${gradeValue === 'admis' ? 'selected' : ''}>admis</option>
                            <option value="respins" ${gradeValue === 'respins' ? 'selected' : ''}>respins</option>
                        </select>
                    `;
                    
                    if (gradeValue) {
                        if (gradeValue === 'admis') {
                            status = '<span class="status_badge passed">admis</span>';
                            passedCount++;
                            totalCredits += creditValue;
                        } else if (gradeValue === 'respins') {
                            status = '<span class="status_badge failed">respins</span>';
                            failedCount++;
                        }
                    } else {
                        pendingCount++;
                    }
                } else {
                    gradeInput = `
                        <input type="number" 
                               min="1" 
                               max="10" 
                               step="1" 
                               value="${gradeValue}" 
                               data-key="${gradeKey}"
                               class="grade-input"
                               onchange="updateGrade(this)">
                    `;
                    
                    if (gradeValue) {
                        const gradeNum = parseInt(gradeValue);
                        if (gradeNum >= 5) {
                            status = '<span class="status_badge passed">promovat</span>';
                            passedCount++;
                            totalCredits += creditValue;
                        } else {
                            status = '<span class="status_badge failed">restanță</span>';
                            failedCount++;
                        }
                    } else {
                        pendingCount++;
                    }
                }
                
                tr.innerHTML = `
                    <td>${materie}</td>
                    <td>${creditValue}</td>
                    <td>${gradeInput}</td>
                    <td>${status}</td>
                `;
                
                gradesTableBody.appendChild(tr);
            });

            if (optionalData) {
                const separatorTr = document.createElement('tr');
                separatorTr.innerHTML = `
                    <td colspan="4" class="optional-separator">
                        <strong style="color: #FF8A8A">materii opționale (alegeți ${optionalData.numar}):</strong>
                    </td>
                `;
                gradesTableBody.appendChild(separatorTr);

                optionalData.optiuni.forEach(materie => {
                    const tr = document.createElement('tr');
                    tr.className = 'optional-subject';
                    const creditValue = getCreditePentruMaterie(materie, cheie, specializare);
                    const gradeKey = `${an}-${semestru}-${materie}`;
                    const gradeValue = note[gradeKey] || '';
                    const isSelected = optionaleSelectate && optionaleSelectate[cheie] && 
                                     optionaleSelectate[cheie].includes(materie);
                    
                    let status = '<span class="status_badge pending">în așteptare</span>';
                    if (gradeValue) {
                        const gradeNum = parseInt(gradeValue);
                        if (gradeNum >= 5) {
                            status = '<span class="status_badge passed">promovat</span>';
                            if (isSelected) {
                                passedCount++;
                                totalCredits += creditValue;
                            }
                        } else {
                            status = '<span class="status_badge failed">restanță</span>';
                            if (isSelected) {
                                failedCount++;
                            }
                        }
                    } else if (isSelected) {
                        pendingCount++;
                    }
                    
                    tr.innerHTML = `
                        <td>
                            <label class="optional-checkbox">
                                <input type="checkbox" 
                                       ${isSelected ? 'checked' : ''} 
                                       data-subject="${materie}"
                                       data-period="${cheie}"
                                       onchange="toggleOptionalSubject(this)">
                                ${materie}
                            </label>
                        </td>
                        <td>${creditValue}</td>
                        <td>
                            <input type="number" 
                                   min="1" 
                                   max="10" 
                                   step="1" 
                                   value="${gradeValue}" 
                                   data-key="${gradeKey}"
                                   class="grade-input"
                                   ${!isSelected ? 'disabled' : ''}
                                   onchange="updateGrade(this)">
                        </td>
                        <td>${status}</td>
                    `;
                    
                    gradesTableBody.appendChild(tr);
                });
            }

            updateAverageDisplay(an, semestru);

            document.getElementById('totalCredits').textContent = totalCredits;
            document.getElementById('passedCount').textContent = passedCount;
            document.getElementById('failedCount').textContent = failedCount;
            document.getElementById('pendingCount').textContent = pendingCount;
            
        } else {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td colspan="4" class="no-subjects">
                    nu există materii definite pentru această perioadă.
                </td>
            `;
            gradesTableBody.appendChild(tr);

            document.getElementById('avgGrade').textContent = '-';
            document.getElementById('totalCredits').textContent = '0';
            document.getElementById('passedCount').textContent = '0';
            document.getElementById('failedCount').textContent = '0';
            document.getElementById('pendingCount').textContent = '0';
        }
        
        updatePredictionSection();
        updateInputStates();
    }

    window.updateGrade = function(input) {
        const key = input.dataset.key;
        const value = input.value;
        
        const parts = key.split('-');
        const materie = parts.slice(2).join('-');
        
        if (isPhysicalEducation(materie)) {
            if (value && !['admis', 'respins'].includes(value)) {
                showToast('pentru educația fizică selectați doar "admis" sau "respins"!', 'error');
                input.value = note[key] || '';
                return;
            }
        } else {
            if (value && (value < 1 || value > 10)) {
                showToast('nota trebuie să fie între 1 și 10!', 'error');
                input.value = note[key] || '';
                return;
            }
        }

        const an = parts[0];
        const semestru = parts[1];

        fetch('/save_nota', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                an: an,
                semestru: semestru,
                materie: materie,
                nota: value || null
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (value) {
                    note[key] = isPhysicalEducation(materie) ? value : parseInt(value);
                } else {
                    delete note[key];
                }

                updateTable();
                showToast(data.msg || 'nota salvată cu succes!');
            } else {
                showToast(data.msg || 'eroare la salvarea notei!', 'error');
                input.value = note[key] || '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('eroare de conexiune!', 'error');
            input.value = note[key] || '';
        });
    };

    window.toggleOptionalSubject = function(checkbox) {
        const subject = checkbox.dataset.subject;
        const period = checkbox.dataset.period;
        const gradeInput = checkbox.closest('tr').querySelector('.grade-input');
        
        if (!optionaleSelectate) {
            optionaleSelectate = {};
        }
        
        if (!optionaleSelectate[period]) {
            optionaleSelectate[period] = [];
        }
        
        if (checkbox.checked) {
            const optionalData = optiuniOptionale[period];
            if (optionalData && optionaleSelectate[period].length >= optionalData.numar) {
                showToast(`puteți selecta maximum ${optionalData.numar} materii opționale pentru această perioadă!`, 'error');
                checkbox.checked = false;
                return;
            }
            
            optionaleSelectate[period].push(subject);
            gradeInput.disabled = false;
        } else {
            const index = optionaleSelectate[period].indexOf(subject);
            if (index > -1) {
                optionaleSelectate[period].splice(index, 1);
            }
            gradeInput.disabled = true;
            gradeInput.value = '';

            const gradeKey = gradeInput.dataset.key;
            updateGrade(gradeInput);
        }
        
        updateTable();
    };

    yearSelect.addEventListener('change', function() {
        const year = yearSelect.value;
        const semester = semesterSelect.value;
        saveDashboardPosition(year, semester);
        checkAvailablePeriods();
        updateTable();
    });

    semesterSelect.addEventListener('change', function() {
        const year = yearSelect.value;
        const semester = semesterSelect.value;
        saveDashboardPosition(year, semester);
        checkAvailablePeriods();
        updateTable();
    });
    
    checkAvailablePeriods();
    updateTable();
});