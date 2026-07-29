/**
 :filename: wexa_statics/js/extras/book/bibbook.js
 :author: Brigitte Bigi
 :contact: contact@sppas.org
 :summary: A class to build the bibliography of a document when its page opens.

 -------------------------------------------------------------------------

 This file is part of Whakerexa: https://github.com/brigitte-bigi/Whakerexa

 Copyright (C) 2023-2026 Brigitte Bigi, CNRS
 Laboratoire Parole et Langage, Aix-en-Provence, France

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.

 This banner notice must not be removed.

 -------------------------------------------------------------------------

 */
'use strict';

import { BibtexSource } from './source.js';
import { BibtexParser } from './parser.js';
import { BibliographyTable } from './bibtable.js';
import { BibliographyError, MissingBibliographyPlace } from './errors.js';

/**
 * Build the bibliography of a document when its page opens.
 *
 * This class is the one that knows in which order the work is done, and it is
 * the only one that does: reading the data, then preparing the references,
 * then composing the bibliography. It is also the only place where an error is
 * caught. Whatever happens, run() never raises: a page that opens a
 * bibliography has nothing to protect itself from, and a document whose data
 * are missing is still a document.
 *
 * Nobody runs anything: the author writes BibTeX entries and text, and the
 * work happens in the browser of whoever opens the page.
 */
export class BookBibliography {
    // FIELDS
    #source;
    #parser;
    #table;
    #placeId;
    #contentId;


    // CONSTRUCTOR
    /**
     * Instantiate the bibliography of a document.
     *
     * @param dataId {string} The id of the element holding the BibTeX data.
     * @param placeId {string} The id of the element where the bibliography goes.
     * @param contentId {string} The id of the element holding the text to read citations from.
     * @param address {string} The address of a BibTeX file, when the data are not in the page.
     */
    constructor(dataId, placeId = 'bibliography', contentId = 'main-content', address = '') {
        this.#source = new BibtexSource(dataId, address);
        this.#parser = new BibtexParser();
        this.#table = new BibliographyTable();
        this.#placeId = placeId;
        this.#contentId = contentId;
    }


    // PUBLIC METHODS
    /**
     * Do the whole work, and never raise.
     *
     * The promise is what the table of contents waits for: the bibliography
     * carries a heading, and has to exist before the headings are gathered.
     *
     * @returns {Promise<void>} Kept once everything is done, or once it cannot be.
     */
    async run() {
        try {
            const content = await this.#source.read();
            const references = this.#parser.parse(content);

            const place = document.getElementById(this.#placeId);
            if (place === null) {
                throw new MissingBibliographyPlace(`No element with id "${this.#placeId}".`);
            }

            place.textContent = '';
            place.appendChild(this.#table.build(references, new Map()));

        } catch (error) {
            if (error instanceof BibliographyError) {
                this.#report(error);
                return;
            }

            throw error;
        }
    }


    // PRIVATE METHODS
    /**
     * Say what went wrong, to whoever wrote the document.
     *
     * The reader is told nothing: a bibliography that could not be built is
     * not their doing, and a page that shouts about it is worse than a page
     * without a bibliography.
     *
     * @param error {BibliographyError} What went wrong.
     * @returns {void}
     */
    #report(error) {
        console.error(`BookBibliography: ${error.message}`);
    }
}
