
сolors_back = [
'rgba(255, 99, 132, 0.2)',
'rgba(54, 162, 235, 0.2)',
'rgba(255, 206, 86, 0.2)',
'rgba(75, 192, 192, 0.2)',
'rgba(153, 102, 255, 0.2)',
'rgba(255, 159, 64, 0.2)'
];
сolors_border = [
'rgba(255, 99, 132, 1)',
'rgba(54, 162, 235, 1)',
'rgba(255, 206, 86, 1)',
'rgba(75, 192, 192, 1)',
'rgba(153, 102, 255, 1)',
'rgba(255, 159, 64, 1)'
];

count_words = [];
name_words = [];
new_color_back = [];
new_color_border = [];
$('.count_tr').each(function () {
    if($(this).children('.count_td').html() > 1){
        name_words.push($(this).children('.count_td_name').html());
        count_words.push($(this).children('.count_td').html());
        new_color_back.push(arrayRandElement(сolors_back));
        new_color_border.push(arrayRandElement(сolors_border));
    }
});

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: name_words,
        datasets: [{
            label: 'Количество',
            data: count_words,
            backgroundColor: new_color_back,
                //borderColor: new_color_border,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
function arrayRandElement(arr) {
    var rand = Math.floor(Math.random() * arr.length);
    return arr[rand];
}

frequency_words_line = [];
name_words_line = [];

$('.count_tr').each(function () {
    name_words_line.push($(this).children('.count_td_name').html());
    frequency_words_line.push($(this).children('.count_td_fr').html());

});

var ctx = document.getElementById('myChart2').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: name_words_line,
        datasets: [{
            label: 'Частота',
            data: frequency_words_line,
                //backgroundColor: new_color_back,
                //borderColor: new_color_border,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

frequency_words_cufa = [];
count_words_cufa = [];
data_cufa = [];
$('.count_tr').each(function () {
    data_cufa.push({'x': $(this).children('.count_td').html(), 'y': $(this).children('.count_td_fr').html()});
});

var ctx = document.getElementById('myChart3').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Частота',
            data: data_cufa,
                //backgroundColor: new_color_back,
                //borderColor: new_color_border,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });


count_words_en = [];
    name_words_en = [];
    new_color_back_en = [];

    $('.count_tr_en').each(function () {
        name_words_en.push($(this).children('.count_td_name_en').html());
        count_words_en.push($(this).children('.count_td_en').html());
        new_color_back_en.push(arrayRandElement(сolors_back));
    });

var ctx = document.getElementById('myChart4').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: name_words_en,
        datasets: [{
            label: 'Количество',
            data: count_words_en,
            backgroundColor: new_color_back_en,
                //borderColor: new_color_border,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    