// Constants
const kckmin = 0.8;
const kckmax = 0.9;
const knmin = 1.1;
const knmax = 1.5;

// Arrays for input variables
let qcr = [];
let vg_T = [];
let V_goods = [];
let T = [];
let Vck1 = [];
let Vck2 = [];
let h = [];
let y = [];
let p = [];
let kpi = [];
let Fck1 = [];
let Fck2 = [];
let Qci = [];
let Fnc1 = [];
let Fnc2 = [];

// Helper function to parse float values
function customParseFloat(value) {
    try {
        value = value.replace(',', '.');
        return parseFloat(value);
    } catch (error) {
        return null;
    }
}

// Function to create cargo input fields
function createCargoInputs(count) {
    const container = document.getElementById('cargoInputs');
    container.innerHTML = '';
    
    // Добавляем общие поля для коэффициентов
    const commonInputs = document.createElement('div');
    commonInputs.className = 'common-inputs';
    commonInputs.innerHTML = `
        <h3>Дополнительные параметры для расчета коэффициентов</h3>
        <div class="form-group">
            <label for="Fl">Площадь непосредственно занятая грузом:</label>
            <input type="number" id="Fl" step="0.01" min="0" required>
            <span class="unit">м²</span>
        </div>
        <div class="form-group">
            <label for="Vf">Среднее количество грузов на складе за период:</label>
            <input type="number" id="Vf" step="0.01" min="0" required>
            <span class="unit">т</span>
        </div>
        <div class="form-group">
            <label for="Qn">Поступление грузов на склад:</label>
            <input type="number" id="Qn" step="0.01" min="0" required>
            <span class="unit">т</span>
        </div>
        <div class="form-group">
            <label for="Qot">Отпуск грузов со склада:</label>
            <input type="number" id="Qot" step="0.01" min="0" required>
            <span class="unit">т</span>
        </div>
        <div class="form-group">
            <label for="T_koef">Период времени для расчета грузопереработки:</label>
            <input type="number" id="T_koef" step="0.01" min="0" required>
            <span class="unit">сут</span>
        </div>
    `;
    container.appendChild(commonInputs);
    
    // Добавляем поля для каждого груза
    for (let i = 0; i < count; i++) {
        const cargoDiv = document.createElement('div');
        cargoDiv.className = 'cargo-inputs';
        cargoDiv.setAttribute('data-index', i);
        
        cargoDiv.innerHTML = `
            <h3>Груз ${i + 1}</h3>
            <div class="form-group">
                <label for="qcr${i}">Расчётный суточный грузопоток:</label>
                <input type="number" id="qcr${i}" step="0.01" min="0" required>
                <span class="unit">т/сут</span>
            </div>
            <div class="form-group">
                <label for="T${i}">Срок хранения:</label>
                <input type="number" id="T${i}" step="0.01" min="0" required>
                <span class="unit">сут</span>
            </div>
            <div class="form-group">
                <label for="p${i}">Удельная нагрузка:</label>
                <select id="p${i}" required>
                    <option value="0.85">0.85 - для крытых складов и платформ общего назначения</option>
                    <option value="0.40">0.40 - для складов тарно-штучных грузов</option>
                    <option value="0.25">0.25 - для специализированных складов</option>
                    <option value="0.50">0.50 - для контейнерных площадок</option>
                    <option value="0.90">0.90 - для площадок тяжеловесных грузов</option>
                    <option value="1.10">1.10 - для площадок навалочных грузов</option>
                </select>
            </div>
            <div class="form-group">
                <label for="kpi${i}">Коэффициент площади складских проездов:</label>
                <select id="kpi${i}" required>
                    <option value="1.7">1.7 - для крытых складов и платформ</option>
                    <option value="2.0">2.0 - для мелких отправок</option>
                    <option value="1.9">1.9 - для контейнерных площадок</option>
                    <option value="1.6">1.6 - для площадок тяжеловесных грузов</option>
                    <option value="1.5">1.5 - для складов угля и минерально-строительных материалов</option>
                </select>
            </div>
            <div class="form-group">
                <label for="Qci${i}">Среднесуточное поступление или отпуск материала:</label>
                <input type="number" id="Qci${i}" step="0.01" min="0" required>
                <span class="unit">т/сут</span>
            </div>
            <div class="form-group">
                <label for="V_goods${i}">Объём груза:</label>
                <input type="number" id="V_goods${i}" step="0.01" min="0" required>
                <span class="unit">т</span>
            </div>
        `;
        
        container.appendChild(cargoDiv);
    }
}

// Function to collect form data
function collectFormData() {
    const count = parseInt(document.getElementById('cargoCount').value);
    qcr = [];
    T = [];
    p = [];
    kpi = [];
    Qci = [];

    for (let i = 0; i < count; i++) {
        qcr.push(parseFloat(document.getElementById(`qcr${i}`).value));
        T.push(parseFloat(document.getElementById(`T${i}`).value));
        const pValue = parseFloat(document.getElementById(`p${i}`).value);
        p.push(pValue);
        kpi.push(parseFloat(document.getElementById(`kpi${i}`).value));
        Qci.push(parseFloat(document.getElementById(`Qci${i}`).value));
    }

    const width = parseFloat(document.getElementById('warehouseWidth').value);
    const goodstype = parseInt(document.getElementById('cargoType').value);

    return { count, width, goodstype };
}

// Функция для отображения коэффициентов отдельно
function displayCoefficients(coefficients) {
    document.getElementById('coefficients').style.display = 'block';
    document.getElementById('k_use_space').innerHTML = `
        <p>При коэф. складируемости 0,8: ${coefficients.k_use_space1}</p>
        <p>При коэф. складируемости 0,9: ${coefficients.k_use_space2}</p>
    `;
    document.getElementById('k_use_v').innerHTML = `
        <p>При коэф. складируемости 0,8: ${coefficients.k_use_v1}</p>
        <p>При коэф. складируемости 0,9: ${coefficients.k_use_v2}</p>
    `;
    document.getElementById('k_ob').innerHTML = `
        <p>При коэф. складируемости 0,8: ${coefficients.k_ob1}</p>
        <p>При коэф. складируемости 0,9: ${coefficients.k_ob2}</p>
    `;
    document.getElementById('Qck').innerHTML = `
        <p>При коэф. складируемости 0,8: ${coefficients.Qck1}</p>
        <p>При коэф. складируемости 0,9: ${coefficients.Qck2}</p>
    `;
}

// Функция для отображения основных результатов
function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    resultsDiv.innerHTML = '<h2>Результаты расчета:</h2>' + results;
}

// Function to calculate warehouse capacity
function calculateWarehouseCapacity() {
    Vck1 = [];
    Vck2 = [];
    
    for (let i = 0; i < qcr.length; i++) {
        Vck1.push(kckmin * qcr[i] * T[i]);
        Vck2.push(kckmax * qcr[i] * T[i]);
    }
    
    return {
        vck1: Vck1.reduce((a, b) => a + b, 0),
        vck2: Vck2.reduce((a, b) => a + b, 0)
    };
}

// Function to calculate warehouse area
function calculateWarehouseArea() {
    Fck1 = [];
    Fck2 = [];
    
    for (let i = 0; i < qcr.length; i++) {
        Fck1.push(kpi[i] * ((kckmin * qcr[i] * T[i]) / p[i]));
        Fck2.push(kpi[i] * ((kckmax * qcr[i] * T[i]) / p[i]));
    }
    
    return {
        fck1: Fck1.reduce((a, b) => a + b, 0),
        fck2: Fck2.reduce((a, b) => a + b, 0)
    };
}

// Function to calculate receiving and sorting area
function calculateReceivingSortingArea() {
    Fnc1 = [];
    Fnc2 = [];
    
    for (let i = 0; i < Qci.length; i++) {
        Fnc1.push((knmin * Qci[i] * T[i]) / p[i]);
        Fnc2.push((kckmax * Qci[i] * T[i]) / p[i]);
    }
    
    return {
        fnc1: Fnc1.reduce((a, b) => a + b, 0),
        fnc2: Fnc2.reduce((a, b) => a + b, 0)
    };
}

// Function to calculate useful area
function calculateUsefulArea(P, kip) {
    const capacity = calculateWarehouseCapacity();
    const Fpol1 = capacity.vck1 / (kip * P);
    const Fpol2 = capacity.vck2 / (kip * P);
    
    return { Fpol1, Fpol2 };
}

// Function to calculate total area
function calculateTotalArea(dV, L, W, kip) {
    const capacity = calculateWarehouseCapacity();
    const nl1 = capacity.vck1 / dV;
    const nl2 = capacity.vck2 / dV;
    const deltaF = L * W * kip;
    const fobsh1 = nl1 * deltaF;
    const fobsh2 = nl2 * deltaF;
    
    return { fobsh1, fobsh2 };
}

// Function to calculate coefficients
function calculateCoefficients(Fl, fobsh1, fobsh2, Vck1, Vck2) {
    const k_use_space1 = Fl / fobsh1;
    const k_use_space2 = Fl / fobsh2;
    
    const Vf = parseFloat(document.getElementById('Vf').value);
    const k_use_v1 = Vf / Vck1.reduce((a, b) => a + b, 0);
    const k_use_v2 = Vf / Vck2.reduce((a, b) => a + b, 0);
    
    const Qn = parseFloat(document.getElementById('Qn').value);
    const Qot = parseFloat(document.getElementById('Qot').value);
    const k_ob1 = (Qn + Qot) / (2 * Vck1.reduce((a, b) => a + b, 0));
    const k_ob2 = (Qn + Qot) / (2 * Vck2.reduce((a, b) => a + b, 0));
    
    const T_koef = parseFloat(document.getElementById('T_koef').value);
    const V_goods = [];
    const vg_T = [];
    
    for (let i = 0; i < a; i++) {
        V_goods.push(parseFloat(document.getElementById(`V_goods${i}`).value));
        vg_T.push(V_goods[i] * T[i]);
    }
    
    const T_average = vg_T.reduce((a, b) => a + b, 0) / V_goods.reduce((a, b) => a + b, 0);
    const Qck1 = Vck1.reduce((a, b) => a + b, 0) * T_koef / T_average;
    const Qck2 = Vck2.reduce((a, b) => a + b, 0) * T_koef / T_average;
    
    return { 
        k_use_space1, k_use_space2,
        k_use_v1, k_use_v2,
        k_ob1, k_ob2,
        Qck1, Qck2
    };
}

// Function to determine kip based on width and goods type
function determineKip(width, goodsType) {
    if (width < 24) {
        return goodsType === 1 ? 0.65 : 0.55;
    } else if (width >= 24 && width < 30) {
        return goodsType === 1 ? 0.7 : 0.6;
    } else {
        return goodsType === 1 ? 0.75 : 0.65;
    }
}

// Main calculation function
function calculate() {
    const { count, width, goodstype } = collectFormData();
    a = count;

    let kip = determineKip(width, goodstype);

    let results = '';
    const capacity = calculateWarehouseCapacity();
    const area = calculateWarehouseArea();
    const receivingArea = calculateReceivingSortingArea();
    const usefulArea = calculateUsefulArea(1, kip);
    const totalArea = calculateTotalArea(1, 1, 1, kip);
    const coefficients = calculateCoefficients(1, totalArea.fobsh1, totalArea.fobsh2, Vck1, Vck2);
    
    results += `<p>Вместимость склада при коэффициенте складируемости 0,8: ${capacity.vck1.toFixed(2)}</p>`;
    results += `<p>Вместимость склада при коэффициенте складируемости 0,9: ${capacity.vck2.toFixed(2)}</p>`;
    results += `<p>Ориентировочная площадь склада при коэф. складируемости 0,8: ${area.fck1.toFixed(2)}</p>`;
    results += `<p>Ориентировочная площадь склада при коэф. складируемости 0,9: ${area.fck2.toFixed(2)}</p>`;
    results += `<p>Площадь приёмо-сортировочных площадок при коэф. складируемости 0,8: ${receivingArea.fnc1.toFixed(2)}</p>`;
    results += `<p>Площадь приёмо-сортировочных площадок при коэф. складируемости 0,9: ${receivingArea.fnc2.toFixed(2)}</p>`;
    results += `<p>Полезная площадь склада при коэф. складируемости 0,8: ${usefulArea.Fpol1.toFixed(2)}</p>`;
    results += `<p>Полезная площадь склада при коэф. складируемости 0,9: ${usefulArea.Fpol2.toFixed(2)}</p>`;
    results += `<p>Общая площадь склада при коэф. складируемости 0,8: ${totalArea.fobsh1.toFixed(2)}</p>`;
    results += `<p>Общая площадь склада при коэф. складируемости 0,9: ${totalArea.fobsh2.toFixed(2)}</p>`;

    displayResults(results);
    // Выводим коэффициенты отдельно
    displayCoefficients({
        k_use_space1: coefficients.k_use_space1.toFixed(2),
        k_use_space2: coefficients.k_use_space2.toFixed(2),
        k_use_v1: coefficients.k_use_v1.toFixed(2),
        k_use_v2: coefficients.k_use_v2.toFixed(2),
        k_ob1: coefficients.k_ob1.toFixed(2),
        k_ob2: coefficients.k_ob2.toFixed(2),
        Qck1: coefficients.Qck1.toFixed(2),
        Qck2: coefficients.Qck2.toFixed(2)
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    const cargoCountInput = document.getElementById('cargoCount');
    cargoCountInput.addEventListener('change', function() {
        createCargoInputs(this.value);
    });

    const form = document.getElementById('warehouseForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        calculate();
    });
});
