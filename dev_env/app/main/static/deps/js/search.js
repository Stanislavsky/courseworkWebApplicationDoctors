document.addEventListener("DOMContentLoaded", function() {
    window.searchByPassport = function() {
        var input, filter, cards, card, passport, i;
        input = document.getElementById("searchInput");
        filter = input.value.trim().toUpperCase(); // Получаем значение поля и преобразуем его в верхний регистр
        cards = document.getElementsByClassName("card");
        var searchResults = document.getElementById("searchResults");
        searchResults.innerHTML = ""; // Очищаем предыдущие результаты поиска

        if (filter === "") {
            // Если поле поиска пустое, просто выходим из функции
            return;
        }

        for (i = 0; i < cards.length; i++) {
            card = cards[i];
            passport = card.getAttribute("data-passport").toUpperCase(); // Получаем значение паспортных данных карточки и преобразуем его в верхний регистр
            if (passport === filter) {
                // Если найдено совпадение, добавляем карточку в результаты поиска
                var clonedCard = card.cloneNode(true);
                clonedCard.querySelector(".button").setAttribute("onclick", "viewPatient('" + passport + "')");
                searchResults.appendChild(clonedCard);
                setTimeout(function() {
                    searchResults.appendChild(clonedCard);
                    
                    setTimeout(function() {
                        clonedCard.classList.remove("hidden");
                    }, 500); 
                }, 1000);

                break; // Прекращаем цикл, так как уже найдено совпадение
            }
        }
    };
});




