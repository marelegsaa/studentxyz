document.addEventListener("DOMContentLoaded", function () {
    console.log("signup.js loaded");
  
    const formular = document.getElementById("formularemail");
    const emailInput = document.getElementById("email");
    const mesajEroare = document.getElementById("email-error");
  
    formular.addEventListener("submit", function (event) {
      const email = emailInput.value.trim();
  
      if (!email.endsWith("@stud.ase.ro")) {
        event.preventDefault();
        mesajEroare.textContent = "e-mailul trebuie să fie de forma nume@stud.ase.ro!";
        mesajEroare.style.display = "block";
      } else {
        mesajEroare.textContent = "";
        mesajEroare.style.display = "none";
      }
    });

    const btnInscrie = document.getElementById("btn-inscrie");

    if (btnInscrie) {
      btnInscrie.addEventListener("click", function () {
        const inscriereUrl = btnInscrie.getAttribute("data-inscriere-url");
        window.location.href = inscriereUrl;
      });
    }

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
  
    specializareSelect.addEventListener("change", function () {
      if (specializareSelect.value) {
        anSelect.style.display = "block";
      } else {
        anSelect.style.display = "none";
      }
    });
  });