const cardsData = [
    {
        image: "https://tolstoy.ru/upload/creativity/fiction/detail/upload/iblock/72e/w-p.jpg",
        title: "Война и мир",
        description: "Роман-эпопея Льва Толстого",
        fullDescription: "«Война́ и мир» — роман-эпопея Льва Николаевича Толстого, описывающий русское общество в эпоху войн против Наполеона в 1805—1812 годах."
    },
    {
        image: "https://cdn.azbooka.ru/cv/w1100/744e11e8-81a5-41ff-92ff-784d2166f3b3.jpg",
        title: "Преступление и наказание",
        description: "Роман Фёдора Достоевского",
        fullDescription: "«Преступле́ние и наказа́ние» — роман Фёдора Михайловича Достоевского, впервые опубликованный в 1866 году."
    },
    {
        image: "https://cdn.azbooka.ru/cv/w1100/98fa6b42-e86d-4f17-9376-25e98cc784e5.jpg",
        title: "Мастер и Маргарита",
        description: "Роман Михаила Булгакова",
        fullDescription: "«Ма́стер и Маргари́та» — роман Михаила Афанасьевича Булгакова, работа над которым началась в конце 1920-х годов и продолжалась вплоть до смерти писателя."
    },
    {
        image: "https://cdn.litres.ru/pub/c/cover/69298261.jpg",
        title: "1984",
        description: "Роман-антиутопия Джорджа Оруэлла",
        fullDescription: "«1984» — роман-антиутопия Джорджа Оруэлла, изданный в 1949 году, который описывает тоталитарное общество в условиях жёсткого контроля."
    },
    {
        image: "https://m.media-amazon.com/images/I/81nQCDT-sXL._UF1000,1000_QL80_.jpg",
        title: "Гарри Поттер",
        description: "Серия романов Дж. К. Роулинг",
        fullDescription: "«Га́рри По́ттер» — серия из семи романов, написанных британской писательницей Дж. К. Роулинг."
    },
    {
        image: "https://nukadeti.ru/content/images/essence/tale/5506/84.jpg",
        title: "Маленький принц",
        description: "Повесть Антуана де Сент-Экзюпери",
        fullDescription: "«Маленький принц» — аллегорическая повесть-сказка Антуана де Сент-Экзюпери, впервые опубликованная в 1943 году."
    }
];

const cardsContainer = document.getElementById('cardsContainer');
const modal = document.getElementById('modal');
const closeBtn = document.querySelector('.close');

function renderCards() {
    cardsContainer.innerHTML = cardsData.map(card => `
        <div class="card">
            <img src="${card.image}" alt="${card.title}">
            <h2>${card.title}</h2>
            <p>${card.description}</p>
            <button class="details-btn" onclick="openModal('${card.image}', '${card.title}', '${card.fullDescription}')">
                Подробнее
            </button>
        </div>
    `).join('');
}

function openModal(image, title, description) {
    document.getElementById('modalImage').src = image;
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalDescription').textContent = description;
    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
}

closeBtn.addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});

// Инициализация
renderCards();