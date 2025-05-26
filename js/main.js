(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-dark shadow navbar-gradient');
            } else {
                $('.fixed-top').removeClass('bg-dark shadow navbar-gradient');
            }
        } else {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-dark shadow navbar-gradient').css('top', -45);
            } else {
                $('.fixed-top').removeClass('bg-dark shadow navbar-gradient').css('top', 0);
            }
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return false;
    });

    // Mobile menu close button
    $(document).on('click', '.menu-close', function () {
        $('.navbar-collapse').collapse('hide');
    });

    // Causes progress
    $('.causes-progress').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: false,
        smartSpeed: 1000,
        center: true,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            }
        }
    });

    // Counter Animation
    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000; // 2 seconds
        const step = target / (duration / 16); // 60fps
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                element.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    }

    // Intersection Observer for counters
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                animateCounter(counter);
                counterObserver.unobserve(counter);
            }
        });
    }, {
        threshold: 0.5
    });

    // Initialize counters
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.counter-value').forEach(counter => {
            counterObserver.observe(counter);
        });

        // Initialize Child Welfare Chart
        const ctx = document.getElementById('childWelfareChart');
        if (ctx) {
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['2018', '2019', '2020', '2021', '2022', '2023'],
                    datasets: [{
                        label: 'Education Gap (Millions)',
                        data: [262, 260, 258, 259, 258, 258],
                        borderColor: '#00704A',
                        tension: 0.4,
                        fill: false
                    }, {
                        label: 'Healthcare Access (Millions)',
                        data: [420, 415, 410, 405, 402, 400],
                        borderColor: '#00B98E',
                        tension: 0.4,
                        fill: false
                    }, {
                        label: 'Orphaned Children (Millions)',
                        data: [150, 148, 146, 144, 142, 140],
                        borderColor: '#0F172B',
                        tension: 0.4,
                        fill: false
                    }, {
                        label: 'Food Insecurity (Millions)',
                        data: [360, 355, 350, 348, 346, 345],
                        borderColor: '#FF6B6B',
                        tension: 0.4,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Global Child Welfare Trends (2018-2023)'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Number of Children (Millions)'
                            }
                        }
                    }
                }
            });

            // Add animation to the chart
            let currentYear = 2018;
            const updateInterval = 2000; // Update every 2 seconds

            function updateChart() {
                const newData = chart.data.datasets.map(dataset => {
                    const currentValue = dataset.data[dataset.data.length - 1];
                    const randomChange = (Math.random() - 0.5) * 2; // Random change between -1 and 1
                    return [...dataset.data, currentValue + randomChange];
                });

                chart.data.labels.push((currentYear + 1).toString());
                chart.data.datasets.forEach((dataset, index) => {
                    dataset.data = newData[index];
                });

                // Remove oldest data point if we have more than 6 years
                if (chart.data.labels.length > 6) {
                    chart.data.labels.shift();
                    chart.data.datasets.forEach(dataset => {
                        dataset.data.shift();
                    });
                }

                currentYear++;
                chart.update();
            }

            // Start the live updates
            setInterval(updateChart, updateInterval);
        }
    });

})(jQuery);

