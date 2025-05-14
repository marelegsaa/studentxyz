document.addEventListener("DOMContentLoaded", function () {
    console.log("signup.js loaded");

    document.getElementById('formularemail')?.addEventListener('submit', function(e) {
    const email = document.getElementById('email').value;
    const emailError = document.getElementById('email-error');
    
    if (!email.endsWith('@stud.ase.ro')) {
        e.preventDefault();
        emailError.textContent = 'trebuie să folosești un email instituțional (@stud.ase.ro)';
        return false;
    }
    return true;
  });

  document.getElementById('email')?.addEventListener('input', function() {
    document.getElementById('email-error').textContent = '';
  });

    document.getElementById('btn-inscrie')?.addEventListener('click', function(e) {
        e.preventDefault();
        const signupUrl = this.getAttribute('data-signup-url');
        window.location.href = signupUrl;
    });

    const facultateSelect = document.getElementById("facultate");
    const specializareSelect = document.getElementById("specializare");
    const anSelect = document.getElementById("an");
  
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
  
    if (facultateSelect) {
        facultateSelect.addEventListener("change", function () {
            const selected = facultateSelect.value;
            specializareSelect.innerHTML = '<option value="">--selectează specializarea--</option>';
            specializareSelect.style.display = "none";
            anSelect.style.display = "none";
    
            if (specializari[selected]) {
                specializari[selected].forEach(function (spec) {
                    const opt = document.createElement("option");
                    opt.value = spec;
                    opt.textContent = spec;
                    specializareSelect.appendChild(opt);
                });
                specializareSelect.style.display = "block";
            }
        });
    }
  
    if (specializareSelect) {
        specializareSelect.addEventListener("change", function () {
            if (specializareSelect.value) {
                anSelect.style.display = "block";
            } else {
                anSelect.style.display = "none";
            }
        });
    }
  });