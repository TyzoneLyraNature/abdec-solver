// Web Worker
import { solve as solveExactCover } from 'dlxlib';
import PolyominoProblem from './PolyominoProblem';
import { Polyomino } from './Polyomino';

self.onmessage = function(event) {

    let { _, problem } = event.data;
    let polyProblem = new PolyominoProblem(
        problem.pieces.map(coords => new Polyomino(coords)),
        new Polyomino(problem.region),
        problem.allowRotation,
        problem.allowReflection
    );

    const totalPieceCoords = polyProblem.pieces.reduce((sum, p) => sum + p.coords.length, 0);
    const totalRegionCoords = polyProblem.region.coords.length;
    if (totalPieceCoords > totalRegionCoords) {
        // Trivially non-solvable
        return self.postMessage({ solution: null, time: 0 });
    }

    let startTime = performance.now();

    //Dlx only now

    let { convertedProblem, interpreter } = polyProblem.convertToDlx();

    let { matrix } = convertedProblem;

    let solutions = solveExactCover(matrix, null, null, 1);

    if (solutions.length == 0) {
        self.postMessage({ solution: null, time: performance.now() - startTime });
    } else {
        let rows = solutions[0].map(i => matrix[i]);
        let solution = [ polyProblem.region, ...interpreter(rows) ];
        self.postMessage({ solution, time: performance.now() - startTime });
    }


};
