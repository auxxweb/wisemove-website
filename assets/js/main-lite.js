(function ($) {
    'use strict';

    function preloader() {
        $('#preloader').stop(true).fadeOut(150);
    }

    function offcanvasMenu() {
        $('.menu-tigger').on('click', function () {
            $('.offCanvas__info, .offCanvas__overly').addClass('active');
            return false;
        });
        $('.menu-close, .offCanvas__overly').on('click', function () {
            $('.offCanvas__info, .offCanvas__overly').removeClass('active');
        });
    }

    function dataBackground() {
        $('[data-background]').each(function () {
            $(this).css('background-image', 'url(' + $(this).attr('data-background') + ')');
        });
    }

    function progressPageLoad() {
        var progressWrap = document.querySelector('.btn-scroll-top');
        if (progressWrap == null) return;
        var progressPath = document.querySelector('.btn-scroll-top path');
        if (!progressPath) return;
        var pathLength = progressPath.getTotalLength();
        var offset = 50;
        progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
        progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
        progressPath.style.strokeDashoffset = pathLength;
        progressPath.getBoundingClientRect();
        progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
        window.addEventListener('scroll', function () {
            var scroll = document.body.scrollTop || document.documentElement.scrollTop;
            var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            var progress = pathLength - (scroll * pathLength) / height;
            progressPath.style.strokeDashoffset = progress;
            var scrollElementPos = document.body.scrollTop || document.documentElement.scrollTop;
            if (scrollElementPos >= offset) {
                progressWrap.classList.add('active-progress');
            } else {
                progressWrap.classList.remove('active-progress');
            }
        });
        progressWrap.addEventListener('click', function (e) {
            e.preventDefault();
            window.scroll({ top: 0, left: 0, behavior: 'smooth' });
        });
    }

    function inputFocus() {
        $('input, textarea, select')
            .focus(function () {
                $(this).closest('div.input-group').addClass('focus');
            })
            .blur(function () {
                $(this).closest('div.input-group').removeClass('focus');
            });
    }

    function mobileHeaderActive() {
        var navbarTrigger = $('.burger-icon'),
            endTrigger = $('.mobile-menu-close'),
            container = $('.mobile-header-active'),
            wrapper4 = $('body');
        if (!wrapper4.find('.body-overlay-1').length) {
            wrapper4.prepend('<div class="body-overlay-1"></div>');
        }
        navbarTrigger.on('click', function (e) {
            e.preventDefault();
            navbarTrigger.toggleClass('burger-close');
            container.toggleClass('mobile-menu-active');
        });
        endTrigger.on('click', function () {
            container.removeClass('mobile-menu-active');
            navbarTrigger.removeClass('burger-close');
        });
        var $offCanvasNav = $('.mobile-menu'),
            $offCanvasNavSubMenu = $offCanvasNav.find('.sub-menu');
        $offCanvasNavSubMenu.parent().prepend('<span class="menu-expand"><i class="arrow-small-down"></i></span>');
        $offCanvasNavSubMenu.slideUp();
        $offCanvasNav.on('click', 'li a, li .menu-expand', function (e) {
            var $this = $(this);
            if (
                $this.parent().attr('class') &&
                $this.parent().attr('class').match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/) &&
                ($this.attr('href') === '#' || $this.hasClass('menu-expand'))
            ) {
                e.preventDefault();
                if ($this.siblings('ul:visible').length) {
                    $this.parent('li').removeClass('active');
                    $this.siblings('ul').slideUp();
                } else {
                    $this.parent('li').addClass('active');
                    $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
                    $this.closest('li').siblings('li').find('ul:visible').slideUp();
                    $this.siblings('ul').slideDown();
                }
            }
        });
    }

    function cardScroll() {
        if (!$('.cards').length || typeof aat === 'undefined') return;
        const { ScrollObserver, valueAtPercentage } = aat;
        const cardsContainer = document.querySelector('.cards');
        const cards = document.querySelectorAll('.card-custom');
        cardsContainer.style.setProperty('--cards-count', cards.length);
        cardsContainer.style.setProperty('--card-height', `${cards[0].clientHeight}px`);
        Array.from(cards).forEach((card, index) => {
            const offsetTop = 20 + index * 20;
            card.style.paddingTop = `${offsetTop}px`;
            if (index === cards.length - 1) return;
            const toScale = 1 - (cards.length - 1 - index) * 0.1;
            const nextCard = cards[index + 1];
            const cardInner = card.querySelector('.card__inner');
            ScrollObserver.Element(nextCard, {
                offsetTop,
                offsetBottom: window.innerHeight - card.clientHeight,
            }).onScroll(({ percentageY }) => {
                cardInner.style.scale = valueAtPercentage({
                    from: 1,
                    to: toScale,
                    percentage: percentageY,
                });
                cardInner.style.filter = `brightness(${valueAtPercentage({
                    from: 1,
                    to: 0.6,
                    percentage: percentageY,
                })})`;
            });
        });
    }

    $(function () {
        preloader();
        progressPageLoad();
        offcanvasMenu();
        dataBackground();
        mobileHeaderActive();
        inputFocus();
    });

    $(window).on('load', function () {
        cardScroll();
    });
})(jQuery);
