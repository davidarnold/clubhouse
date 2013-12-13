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
$.fn.dirty = function (saveButtonSelector, initiallyDirty) {
    var $form = $(this),
        $saveButton = $(saveButtonSelector),
        dirty = function () {
            $form.data('formDirty', 'dirty');
            $saveButton.text('Save Changes').removeClass('btn-success').addClass('btn-danger');
        };

    if (initiallyDirty) {
        dirty();
    }

    $(window).on('beforeunload', function (event) {
        if ($form.data('formDirty')) {
            return "You have unsaved changes.";
        }
    });

    $saveButton.click(function () {
        $form.removeData('formDirty');
        $saveButton.text('Save Changes').removeClass('btn-danger').addClass('btn-success');
        $(this).button('loading');
    });

    $form.on(
        'click', 'button[type="button"]', dirty
    ).on(
        'keypress', 'input,textarea', dirty
    ).on(
        'keydown', 'input,textarea', function (event) {
            // Backspace
            if (event.which === 8) {
                dirty();
            }
        }
    ).on(
        'paste', 'input,textarea', dirty
    ).on(
        'change', 'select,input[type="checkbox"],input[type="radio"]', dirty
    );
};