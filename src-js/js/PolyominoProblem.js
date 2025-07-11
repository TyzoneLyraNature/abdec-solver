import { Polyomino } from './Polyomino.js';

export default class PolyominoProblem {

    constructor(pieces, region, allowRotation=true, allowReflection=false) {
        this.pieces = pieces.map(x => x.normalize());
        this.region = region.normalize();
        this.allowRotation = allowRotation;
        this.allowReflection = allowReflection;

        // Extremal bounds
        this.width = this.region.getWidth();
        this.height = this.region.getHeight();
    }

    _fits(piece) {
        if (piece.getLargestX() < this.width && piece.getLargestY() < this.height) {
            // It's possible
            // Check that every coordinate is actually in the region
            return piece.coords.every(c => this.region.containsCoordinate(c));
        } else {
            return false;
        }
    }

    * _generateAllPossibleConfigurations(piece) {
        let uniqueConfigs = [];

        for (let rotation of [ 0, ...(this.allowRotation ? [1, 2, 3] : []) ]) {
            for (let reflected of [ false, ...(this.allowReflection ? [ true ] : []) ]) {
                let config = piece.rotate(rotation);
                if (reflected) config = config.reflect();
                config = config.normalize();

                // Account for symmetries
                // Two configs are the same iff their normalizations are equal
                if (uniqueConfigs.some(c => c.equals(config))) {
                    continue;
                } else {
                    uniqueConfigs.push(config);
                }

                for (let dx = 0; dx < this.width; dx ++) {
                    for (let dy = 0; dy < this.height; dy ++) {
                        let place = config.translate(dx, dy);
                        if (this._fits(place)) yield place;
                    }
                }
            }
        }

    }

    convertToDlx() {
        let matrix = [];

        const totalPieceCoords = this.pieces.reduce((sum, p) => sum + p.coords.length, 0);
        const totalRegionCoords = this.region.coords.length;
        const numPlaceholders = Math.max(totalRegionCoords - totalPieceCoords, 0);

        // Add single-block placeholder pieces so that the total count of blocks 
        // adds up to that of the destination region, so we can make this an *exact* problem
        let paddedPieces = [ ...this.pieces, ...(new Array(numPlaceholders).fill(new Polyomino([ [0, 0] ]))) ];

        // Columns are indexed by pieces followed by region coordinates:
        // p_1 p_2 p_3 ... p_n | (x0, y0) (x1, y1) (x2, y2) ... (xk, yk)

        // Each row will assert that piece p_i may exist at certain coordinates in the region, which
        // is indicated by placing a 1 at column p_i and 1's at the columns of the coordinates it occupies.
        // A solution is then a subset of rows so that 1 appears exactly once in each column.

        let rowSize = paddedPieces.length + this.region.coords.length;

        paddedPieces.forEach((piece, pieceIndex) => {
            let configs = Array.from(this._generateAllPossibleConfigurations(piece));
            for (let config of configs) {
                let row = new Array(rowSize).fill(0);

                row[pieceIndex] = 1;

                for (let c of config.coords) {
                    let index = this.region.coords.findIndex(x => c[0] == x[0] && c[1] == x[1]);
                    row[paddedPieces.length + index] = 1;
                }

                matrix.push(row);
            }
        });

        let findOneIndices = arr => {
            let next = arr.indexOf(1);
            if (next < 0) return [];
            return [ next, ...findOneIndices(arr.slice(next + 1)).map(i => next + 1 + i) ];
        }

        let interpreter = solution => {
            let pieces = [];
            for (let row of solution) {
                const pieceIndex = row.indexOf(1);
                const coordIndices = findOneIndices(row.slice(paddedPieces.length));
                if (pieceIndex < this.pieces.length) {
                    // Only account for the user's pieces, not the placeholder blocks.
                    pieces.push(new Polyomino(coordIndices.map(i => this.region.coords[i])));
                }
            }
            return pieces;
        }

        return { convertedProblem: { matrix }, interpreter };
    }

}
