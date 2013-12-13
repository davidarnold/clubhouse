/*
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the License in the included LICENSE.txt
 * or http://opensource.org/licenses/CDDL-1.0
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When modifying Covered Code, update the affected files' copyright
 * notice with the current year and add your name to its contributors
 * list.
 *
 * Copyright 2012-2013 Clubhouse Contributors
 *
 * File contributors: David Arnold
 */
$(document).ready(function () {
    var $filters = $('[data-action="filter"]');

    $filters.each(function () {
        var $this = $(this),
            selector = $this.data('filterSelector'),
            $elements = $(selector);

        $this.change(function() {
            var tag = $this.val();

            if (tag) {
                $elements.filter('[data-filter-tags~="' + tag + '"]').slideDown();
                $elements.filter(':not([data-filter-tags~="' + tag + '"])').slideUp();
            } else {
                $elements.slideDown();
            }
        });
    });
});