document.addEventListener('DOMContentLoaded', function() {
    const facultateSelect = document.querySelector('select[name="facultate"]');
    const specializareSelect = document.querySelector('select[name="specializare"]');
    const promotieSelect = document.querySelector('select[name="promotie"]');

    const specializari = {
        csie: [
            "cibernetică economică",
            "informatică economică",
            "statistică și previziune economică"
        ],
        finante: [
            "finanțe și bănci",
            "asigurări și reasigurări",
            "piețe de capital"
        ],
        marketing: [
            "marketing",
            "comunicare și relații publice",
            "marketing internațional"
        ],
        comert: [
            "comerț",
            "turism și servicii",
            "logistică"
        ],
        economie: [
            "economie generală",
            "dezvoltare durabilă",
            "economie și politici publice"
        ],
        contabilitate: [
            "contabilitate și informatică de gestiune",
            "audit financiar",
            "control și expertiză contabilă"
        ],
        management: [
            "management",
            "antreprenoriat",
            "managementul resurselor umane"
        ],
        rei: [
            "relații economice internaționale",
            "afaceri internaționale",
            "diplomație economică"
        ],
        fabiz: [
            "business administration - english",
            "administration des affaires - français",
            "unternehmensführung - deutsch"
        ]
    };
    
    function updateSpecializari() {
        if (!facultateSelect || !specializareSelect) return;

        const selectedFacultate = facultateSelect.value;
        const selectedPromotie = promotieSelect ? promotieSelect.value : '';
        
        const currentVal = specializareSelect.value || (typeof currentSpecialization !== 'undefined' ? currentSpecialization : '');

        specializareSelect.innerHTML = '';

        if (!selectedFacultate) return;

        let listaSpec = specializari[selectedFacultate] || [];

        if (selectedFacultate === 'csie') {
            if (selectedPromotie === '2025-2028') {
                listaSpec = [
                    "cibernetică economică",
                    "informatică economică",
                    "statistică economică și data science"
                ];
            } else {
                listaSpec = [
                    "cibernetică economică",
                    "informatică economică",
                    "statistică și previziune economică"
                ];
            }
        }

        if (listaSpec.length > 0) {
            listaSpec.forEach(function(spec) {
                const opt = document.createElement('option');
                opt.value = spec;
                opt.textContent = spec;

                if (spec === currentVal) {
                    opt.selected = true;
                }
                
                specializareSelect.appendChild(opt);
            });
        }
    }

    if (facultateSelect && specializareSelect) {
        updateSpecializari();

        facultateSelect.addEventListener('change', updateSpecializari);

        if (promotieSelect) {
            promotieSelect.addEventListener('change', updateSpecializari);
        }
    }

    const flashMessages = document.querySelectorAll('.flash-messages > div');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);