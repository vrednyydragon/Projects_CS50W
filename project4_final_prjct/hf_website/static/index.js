// scroll page
window.addEventListener('scroll', () => {
    if ($(this).scrollTop() > 150) {
        document.querySelector('#scrollTop').hidden = false;
    }
    else{
        document.querySelector('#scrollTop').hidden = true;
    }
});

document.addEventListener('DOMContentLoaded', () => {
    btn_wiev();
    var doc_url = document.URL;

    // slow scroll page
    document.querySelector('#scrollTop').onclick = () => {
        $('html, body').stop().animate({scrollTop : 0}, 300);
    };

    // put current info into user profile
    if ( doc_url.includes("http://127.0.0.1:8000/profile") ){
        btn_wiev()
        var user_gender = document.getElementsByName("gender");
        var gender_id = user_gender[0].id;
        if (gender_id) {
            user_gender[0].value = gender_id;
            user_gender[0].disabled = true;
            $("#user_age_string")[0].hidden = false;
            document.getElementsByName("date_of_birth")[0].disabled = true;
            document.getElementsByName("user_height")[0].disabled = true;
            document.getElementsByName("user_weight")[0].disabled = true;
            $("#us_profile_submit")[0].hidden = true;
            $("#cansel_btn")[0].hidden = true;
            $("#us_profile_change_btn")[0].hidden = false;
        }
        console.log($('#curr_user_picture')[0].src);
        if ($('#curr_user_picture')[0].src == "http://127.0.0.1:8000/profile") {
            change_m_w_img(user_gender[0].value);
        }
        document.querySelector('select').onchange = () => {
            var selected = user_gender[0].value;
            if ($('#curr_user_picture')[0].src.includes("static")) {
                change_m_w_img(selected);
            }
        };
        var type_of_food = document.getElementsByName("type_of_food");
        var type_id = type_of_food[0].id;
        if (type_id) {
            type_of_food[0].value = type_id;
            type_of_food[0].disabled = true;
            // type_of_food[0].setAttribute("disabled", "disabled");
        }
        var activity_level = document.getElementsByName("activity_level");
        var activity_id = activity_level[0].id;
        if (activity_id) {
            activity_level[0].value = activity_id;
            activity_level[0].disabled = true;
            // activity_level[0].setAttribute("disabled", "disabled");
        }

        document.querySelector("#us_profile_change_btn").onclick = () => {
            $("#us_profile_change_btn")[0].hidden = true;
            $("#us_profile_submit")[0].hidden = false;
            $("#cansel_btn")[0].hidden = false;
            document.getElementsByName("date_of_birth")[0].disabled = false;
            document.getElementsByName("gender")[0].disabled = false;
            document.getElementsByName("user_height")[0].disabled = false;
            document.getElementsByName("user_weight")[0].disabled = false;
            document.getElementsByName("type_of_food")[0].disabled = false;
            document.getElementsByName("activity_level")[0].disabled = false;
            document.getElementById("user_img_name_change_btn").hidden = true;
        };

        // change photo /name in user profile
        document.querySelector('#user_img_name_change_btn').onclick = () => {
            document.getElementById("user_img_name_normal").className += " hide_elem";
            document.getElementById("user_img_name_changeform").style.removeProperty("display");
            document.getElementById("us_profile_change_btn").hidden = true;
        };

        document.querySelectorAll('.cansel_btn').forEach(function(button) {
            button.onclick = cansel;
        });
        document.getElementsByClassName("openbtn")[0].onclick = openNav;
        document.getElementsByClassName("closebtn")[0].onclick = closeNav;
    }


    if ( doc_url.includes("http://127.0.0.1:8000/calculator") ){
        btn_wiev()
        var calc_age = document.getElementsByName('age')[0];
        var calc_height = document.getElementsByName('user_height')[0];
        var calc_weight = document.getElementsByName('user_weight')[0];
        var calc_type_food = document.getElementsByName('type_of_food')[0];
        var calc_activity = document.getElementsByName('activity_level')[0];
        document.querySelector('#calc_clear').onclick = function () {
            calc_age.value = "";
            calc_height.value = "";
            calc_weight.value = "";
        };
        document.querySelector('#calc_submit').onclick = () => {
            var calc_gender = $('input[name=gender]:checked').val();
            console.log(calc_gender);

            var bmr = 9.99 * Number(calc_weight.value) + 6.25 * Number(calc_height.value) - 4.92 * Number(calc_age.value);
            var bmr_finish = 0;
            const man_coeff = 5;
            const woman_coeff = 161;
            const with_type_food = 0.2;
            const water_coeff = 30;
            const sugar_coeff = 0.05;
            console.log(calc_age.value, calc_height.value,
                calc_weight.value, calc_gender,
                calc_type_food.value, calc_activity.value);
            if (calc_gender == "female") {
                bmr -= woman_coeff;
            }
            else {
                bmr += man_coeff;
            }
            bmr *= calc_activity.value;
            if (calc_type_food.value == "weight_loss") {
                bmr_finish = bmr - (bmr * with_type_food)
                //proteins/carb/fats in % = 30/20/50
                var dict = prot_fat_carb(0.3, 0.2, 0.5, bmr_finish);
                console.log(dict);
            }
            else if (calc_type_food.value == "muscle_gain") {
                bmr_finish = bmr + (bmr * with_type_food)
                //proteins/carb/fats in % = 35/30/55
                var dict = prot_fat_carb(0.35, 0.3, 0.55, bmr_finish);
                console.log(dict);
            }
            else if (calc_type_food.value == "weight_maintenance") {
                bmr_finish = bmr
                //proteins/carb/fats in % = 30/30/40
                var dict = prot_fat_carb(0.3, 0.3, 0.4, bmr_finish);
                console.log(dict);
            }
            // console.log(bmr_finish); //Kkalories
            var calc_water = water_coeff * calc_weight.value / 1000;//daily water
            var calc_sugar = sugar_coeff * bmr_finish / 4; //daily sugar
            // put current result into calculator page
            document.querySelector('#res_calories').innerHTML = Math.round(bmr_finish);
            document.querySelector('#res_water').innerHTML = rounded(calc_water);
            document.querySelector('#res_proteins').innerHTML = Math.round(dict['calc_protein']);
            document.querySelector('#res_fat').innerHTML = Math.round(dict['calc_fat']);
            document.querySelector('#res_carb').innerHTML = Math.round(dict['calc_carb']);
            document.querySelector('#res_sugar').innerHTML = Math.round(calc_sugar);

            //Нормы БЖУ:
            // белки — 1.5-2.5 г на кг веса тела
            // жиры — 0.8-1.5 г жиров на 1 кг веса
            // углеводы — 2 г углеводов на 1 кг веса (спортсмены могут увеличивать эту норму в 2 и более раз)

            // Помимо суточных норм, контролировать рацион помогают еще и пропорции нутриентов. Разделим их на три вида:
            // Для здорового питания. Стандартом считается соотношение 3/3/4, то есть по 30% рациона составляют белки и жиры, и 40% - углеводы.
            // Для похудения. Чтобы сбросить вес, нужно уменьшить количество потребляемых жиров в пользу углеводов.
            //                 Так что последние должны составлять половину рациона, белки - от 25 до 35%, а жиры - не более 30%.
            // Для набора массы. В этом случае опять же нужны углеводы (тренировки требуют большого количества энергии) и белки
            //             (мышцы складываются именно из них). Получаем пропорцию 35/30/55. Отмечается также, что перед набором
            //              массы нужно убедиться в отсутствии избытков жира. Иными словами, сначала худеем и сжигаем жир, а потом наращиваем мышцы.
        // }
        };
    }

    if ( doc_url.includes("http://127.0.0.1:8000/recipes") ){
        btn_wiev();
        changeBackground('#343a40');
        curr_recipes_view();
        if  ($("#pagin_pages_btn")[0].children[0]){
            if ( doc_url.includes("/recipes")){
                $("#pagin_pages_btn")[0].children[0].className += " active";
            }
        }

    // get list for quick searching in recipes
        $.ajax({
            url: doc_url,
            type: 'get',
            success: function (data) {
                if (data.recipe_list) {
                    sessionStorage.setItem("names_for_search", JSON.stringify(data.recipe_list));
                }
            }
        });
        // coloring current pagination button page btn
        if (doc_url.includes("?page=")){
            for (let n = 1; n <= $("#pagin_pages_btn")[0].childElementCount; n++) {
                var page_numb = n;
                if (doc_url.includes("?page=" + page_numb)) {
                    for (let i = 0; i <= $("#pagin_pages_btn")[0].childElementCount-1; i++) {
                        if (parseInt($("#pagin_pages_btn")[0].children[i].innerText) == page_numb) {
                            $("#pagin_pages_btn")[0].children[0].classList.remove("active");
                            $("#pagin_pages_btn")[0].children[i].className += " active";
                        }
                    }
                }
            }
        }

        // change view of recipes by tile or list by button
        document.querySelector("#list_view_btn").onclick = () => {
            document.querySelector('#all_recipes_list').hidden = false;
            document.querySelector('#all_recipes_tile').hidden = true;
            sessionStorage.setItem("recipes_view", "list");
        };
        document.querySelector("#tile_view_btn").onclick = () => {
            document.querySelector('#all_recipes_list').hidden = true;
            document.querySelector('#all_recipes_tile').hidden = false;
            sessionStorage.setItem("recipes_view", "tile");
        };

        // show 5 li in recipe preview
        var recip_pg_list = document.getElementsByClassName('ing_list_recipes_pg_cl');
        for (let i=0; i<=(recip_pg_list.length - 1); i++){
            if (recip_pg_list[i].childElementCount>5){
                while(recip_pg_list[i].childElementCount>5){
                    recip_pg_list[i].lastElementChild.remove();
                }
            }
        }
        let search_data = document.querySelector('#txtSearch');

        search_data.addEventListener('input', () => {
            var div_search_result = document.querySelector("#search_quick_result")
                if (div_search_result.childElementCount != 0){
                    while (div_search_result.firstChild) {
                        div_search_result.removeChild(div_search_result.firstChild);
                    }
                }
            if (search_data.value.length > 2) {
                div_search_result.hidden=false;
                var ul = document.createElement('ul');
                var get_search_list = sessionStorage.names_for_search;
                var all_search_list = JSON.parse(get_search_list);
                // console.log(all_search_list[i]);
                console.log(all_search_list);
                for (let i=0; i<=(all_search_list.length - 1); i++){;
                    if (all_search_list[i]["search_name"].toLocaleLowerCase().includes(search_data.value.toLocaleLowerCase()) && div_search_result.children.length < 5 ){
                        var li = document.createElement('p');
                        var a = document.createElement('a');
                        var search_id = all_search_list[i]["search_id"];
                        a.href = "/one_recipe/" + search_id;
                        li.innerHTML = all_search_list[i]["search_name"];
                        a.appendChild(li);
                        div_search_result.appendChild(a);
                    }
                }
            }
        });
        //all about tags
        var tags_place = document.querySelector("#tags_place");
        $('select').change(function(){
            var tag_value = $(this).val();
            var tag_uid = $(this).children(":selected").attr("id");
            var p = document.createElement('p');
            p.id = "uid" + tag_uid;
            p.innerHTML = tag_value;
            var btn = document.createElement('button');
            btn.className = 'del_tag_btn';
            btn.id = tag_uid;
            btn.innerHTML = 'x';
            tags_place.appendChild(p);
            tags_place.appendChild(btn);
            $.ajax({
                url: doc_url,
                type: 'get',
                data: {"choosen_tag_uid": tag_uid,
                    "choosen_tag_name": tag_value},
                success: function (data) {
                    cansel();
                }
            });
        });
        document.addEventListener('change', () => {
            $('#tags_place').on("click", "button", function () {
                console.log("tag del");
                console.log($(this)[0].id);
                var tag_uid = $(this)[0].id;
                var tag_name_id = "uid" + tag_uid;
                var elem_tag_name = document.querySelector(`#${tag_name_id}`);
                var tag_name = ($(this).val());
                console.log(tag_name)
                tags_place.removeChild($(this)[0]);
                tags_place.removeChild(elem_tag_name)
                $.ajax({
                    url: doc_url,
                    type: 'get',
                    data: {
                        "deleted_tag_uid": tag_uid,
                        "deleted_tag_name": tag_name
                    },
                    success: function (data) {
                        cansel();
                    }
                });
            })
        });
        if (tags_place.childElementCount > 0){
            $('#tags_place').on("click","button", function() {
                console.log("tag del");
                console.log($(this)[0].id);
                var tag_uid = $(this)[0].id;
                var tag_name_id = "uid" + tag_uid;
                var elem_tag_name = document.querySelector(`#${tag_name_id}`);
                var tag_name = ($(this).val());
                console.log(tag_name);
                tags_place.removeChild($(this)[0]);
                tags_place.removeChild(elem_tag_name);
                $.ajax({
                    url: doc_url,
                    type: 'get',
                    data: {"deleted_tag_uid": tag_uid,
                        "deleted_tag_name": tag_name},
                    success: function (data) {
                        cansel();
                    }
                });
             });
        }

        var filter_list = [];
        $("#filter_checkbox").on("click","input", function() {
            var filter_one_value = $(this)[0].value;
            if (filter_list.length == 0){
                filter_list.push(filter_one_value);
                console.log("added");
            }
            else{
                let count = 0;
                for (let i=0; i<=(filter_list.length - 1); i++) {
                    if (filter_list[i] == filter_one_value){
                        filter_list.splice(i,1);
                        var index = i;
                        count += 1;
                        break;
                    }
                }
                if (count == 0){
                    filter_list.push(filter_one_value);
                    console.log("added");

                }
                else if (count == 1){
                    console.log("deleted");
                    filter_list.splice(index,1);
                }

            }
            console.log(filter_list);
            if (sessionStorage["recipes_view"] == "list") {
                let recipes_tags_list = $("tr"); //list of tags by each recipe or product
                for (let n = 0; n <= (recipes_tags_list.length - 1); n++) {
                    for (let i = 0; i <= (filter_list.length - 1); i++) {
                        if (!recipes_tags_list[n].id.includes(filter_list[i])) {
                            recipes_tags_list[n].hidden = true;
                        }
                        else {
                            recipes_tags_list[n].hidden = false;
                        }
                    }
                }
            }
            else if (sessionStorage["recipes_view"] == "tile") {
                let recipes_tags_list = $("span");
                for (let n = 0; n <= (recipes_tags_list.length - 1); n++) {
                    for (let i = 0; i <= (filter_list.length - 1); i++) {
                        if (!recipes_tags_list[n].id.includes(filter_list[i])) {
                            recipes_tags_list[n].hidden = true;
                        }
                        else {
                            recipes_tags_list[n].hidden = false;
                        }
                    }

                }
            }
        });
    }

    if ( doc_url.includes("http://127.0.0.1:8000/one_recipe") ){
        btn_wiev();
        changeBackground('#343a40');
        // add recipe to favorite
        if ( document.querySelector("#fav_recipe_btn") ){
            var btn = document.querySelector("#fav_recipe_btn");
            // console.log(btn.value);
            favorite_btn_color(btn);
            btn.onclick = () => {
                // console.log(`start btn_value = ${btn.value}`);
                if (btn.value === "0"){
                    btn.value = "1";
                    add_in_fav(doc_url);
                }
                else {
                    btn.value = "0";
                    dell_from_fav(doc_url);
                }
                favorite_btn_color(btn);
                // console.log(`finish btn_value = ${btn.value}`);
            }
        }
        // if user didn't register
        if (document.querySelector("#not_registered_fav_btn")) {
            document.querySelector("#not_registered_fav_btn").onclick = () => {
                var login_url = 'http://127.0.0.1:8000/login'; // перевести строку в URL
                var message = 'For adding in favorite you must Login'
                redirect_to_other_page(message, login_url);
            }
        }
        // if user didn't register
        if (document.querySelector("#not_registered_food_log_btn")) {
            document.querySelector("#not_registered_food_log_btn").onclick = () => {
                var login_url = 'http://127.0.0.1:8000/login'; // перевести строку в URL
                var message = 'For adding to the eaten you must Login'
                redirect_to_other_page(message, login_url);
            }
        }
        //if user registered
        if (document.querySelector("#add_food_log_btn")){
            document.querySelector("#add_food_log_btn").onclick = () => {
                var curr_recipe_uid = $("#add_food_log_btn")[0].value;
                console.log(curr_recipe_uid);
                var eaten_weight = $('input').val();
                console.log(eaten_weight);
                var food_time =  $('select').val();
                console.log(food_time);
                $.ajax({
                url: doc_url,
                type: 'get',
                data: {"add_to_eaten": true,
                    "eat_recipe_uid": curr_recipe_uid,
                    "eat_recipe_weight": eaten_weight,
                    "food_time": food_time
                },
                success: () => {
                    alert(eaten_weight + ' g added to eaten!');
                }
                });
            }
        }
        //change nutrics values after input weight
        const input = document.querySelector('#recipeweight');
        const td_nutric_list = $('td');
        input.addEventListener('change', () => {
            nutric_calculator(td_nutric_list)
         });
        // add tag in recipes search
        console.log("link before clicked")
        var tags_link = document.getElementsByClassName("show_tag_name");
        for (let i = 0; i <= (tags_link.length - 1); i++) {
            tags_link[i].onclick = () => {
                console.log("link is clicked");
                console.log(tags_link[i].innerText);
                console.log(tags_link[i].id);
                var tag_value = tags_link[i].innerText;
                var tag_uid = tags_link[i].id;
                $.ajax({
                    url: doc_url,
                    type: 'get',
                    data: {"choosen_tag_uid": tag_uid,
                        "choosen_tag_name": tag_value},
                    success: function (data) {
                        window.open("http://127.0.0.1:8000/recipes");
                    }
                });
            }
        }
    }
    //change website language
    document.querySelector('#ch_lang_en').onclick = () => {
        console.log("change lang on english");
        document.querySelector('#ch_lang_en_li').className += " active";
        document.querySelector('#ch_lang_ru_li').classList.remove("active");
        change_language(doc_url, "en");

        };
    document.querySelector('#ch_lang_ru').onclick = () => {
        console.log("change lang on russian");
        document.querySelector('#ch_lang_ru_li').className += " active";
        document.querySelector('#ch_lang_en_li').classList.remove("active");
        change_language(doc_url, "ru");
    };

    // one product web page
    if ( doc_url.includes("/product/") ) {
        btn_wiev();
        changeBackground('#343a40');
        //change nutrics values after input weight
        const input = document.querySelector('#recipeweight');
        const td_nutric_list = $('td');
        input.addEventListener('change', () => {
            nutric_calculator(td_nutric_list)
        });
    }

});

// Перезагрузить текущую страницу, без использования кэша
function cansel() {
    document.location.reload(true);
}

function openNav() {
    document.getElementById("mySidepanel").style.width = "60%";
    var pr1 = document.getElementById('user_profile1');
    var pr2 = document.getElementById('mySidepanel');
    if (pr2.childElementCount === 1){
        pr2.append(pr1);
    }
}

/* Set the width of the sidebar to 0 (hide it) */
function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
    var pr1 = document.getElementById('user_profile1');
    var pr2 = document.getElementById('profile_main_panel');
    pr2.append(pr1);
    if (pr2.childElementCount == 0){
        pr2.append(pr1);
    }
}

// change male/female image
function change_m_w_img(data) {
    if (data == "female") {
        $('#curr_user_picture').attr("src", "static/woman.jpg");
    }
    else if (data == "male") {
        $('#curr_user_picture').attr("src", "static/man.jpg");
    }
}

function prot_fat_carb(per_prot, per_fat, per_carb, bmr_finish) {
    const protein_kcal = 4; // 1g = 4kcal
    const fat_kcal = 9; // 1g = 9kcal
    const carb_kcal = 4; // 1g = 4kcal
    let dict = {};
    let calc_protein = 0;
    let calc_fat = 0;
    let calc_carb = 0;
    calc_protein = per_prot * bmr_finish / protein_kcal;
    calc_fat = per_fat * bmr_finish / fat_kcal;
    calc_carb = per_carb * bmr_finish / carb_kcal;
    dict = {
        "calc_protein": calc_protein,
        "calc_fat": calc_fat,
        "calc_carb": calc_carb
    };
    return dict
}

// add recipe in users favorite
function add_in_fav(doc_url) {
    $.ajax({
        url: doc_url,
        type: 'get',
        data: {"flag": "true" },
        success: () => {
                alert('Added to favorite!');
        }
    });
}

function dell_from_fav(doc_url) {
    $.ajax({
        url: doc_url,
        type: 'get',
        data: {"flag": "false"},
        success: () => {
                alert('Deleted from favorite!');
        }
    });
}

function favorite_btn_color(btn) {
    if (btn.value === "1"){
            btn.className += " my_background_2";
            btn.setAttribute("title", "Delete from favorite");
        }
        else {
            btn.classList.remove("my_background_2");
            btn.setAttribute("title", "Add to favorite");
        }
}

function change_language(doc_url, lang) {
    $.ajax({
        url: doc_url,
        type: 'get',
        data: {"curr_language": lang},
        // data: JSON.stringify( {"curr_language": lang}),
        success: function (data) {
            console.log(data.current_language);
            sessionStorage.setItem("current_website_lang", JSON.stringify(data.current_language));
            cansel();
        }
    })
}

//change language button view (add this function on each html page)
function btn_wiev() {
    // console.log(sessionStorage.getItem('current_website_lang'));
    if (!sessionStorage.getItem('current_website_lang')) {
        sessionStorage.setItem("current_website_lang", "en");
    }
    // console.log(sessionStorage.getItem('current_website_lang'));
    var curr_lang = sessionStorage.getItem('current_website_lang');
    if (curr_lang.includes("en")) {
        // console.log("en active");
        document.querySelector('#ch_lang_en_li').className += " active";
        document.querySelector('#ch_lang_ru_li').classList.remove("active");
    }
    if (curr_lang.includes("ru")) {
        // console.log("ru active");
        document.querySelector('#ch_lang_ru_li').className += " active";
        document.querySelector('#ch_lang_en_li').classList.remove("active");
    }
}

function changeBackground(color) {
   document.body.style.background = color;
}

//show tile\list recipes view
// change view of recipes by tile or list
function curr_recipes_view() {
    if (!sessionStorage.getItem('recipes_view')) {
            sessionStorage.setItem("recipes_view", "list");
        }
    var curr_view = sessionStorage.getItem('recipes_view');
    if (curr_view.includes("list")) {
        document.querySelector('#all_recipes_list').hidden = false;
        document.querySelector('#all_recipes_tile').hidden = true;
    }
    if (curr_view.includes("tile")) {
        document.querySelector('#all_recipes_list').hidden = true;
        document.querySelector('#all_recipes_tile').hidden = false;
    }
}
function redirect_to_other_page(message, url) {
    if (window.confirm(message)) {
       window.open(url);
    }
}

function rounded(number) {
    return +number.toFixed(2);
}

function nutric_calculator(td_nutric_list) {
    var flex_weight = $('input').val();
    console.log(flex_weight);
    for (let i = 0; i <= (td_nutric_list.length - 1); i++) {
        let origin_value = td_nutric_list[i].id;
        console.log(origin_value);
        td_nutric_list[i].innerHTML = rounded(origin_value / 100 * flex_weight);
    }
}