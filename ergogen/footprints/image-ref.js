// https://github.com/auryn31/avocado/blob/main/ergogen/footprints/avocado.js

module.exports = {
  params: {
    scale: 0.01,
  },
  body: (params) => {
    const allPoints = [
      [
      [135.71806755161285,27.472648487091064],
      [344.32216568120947,363.4669399928282],
      ],
    ].flat();
    const chunks = [];
    let currentChunk = [];
    for (let i = 1; i < allPoints.length; i++) {
      const p1 = allPoints[i - 1];
      const p2 = allPoints[i];
      const distance = Math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2);
      if (distance > 50) {
        chunks.push(currentChunk);
        currentChunk = [];
      } else {
        currentChunk.push(p1);
      }
    }
    chunks.push(currentChunk);

    const pos = ([x, y]) => {
      let xPos = 0;
      let yPos = 0;
      if (params.x === 0) {
        xPos = x * params.scale;
      } else {
        xPos = x * params.scale + params.x;
      }
      if (params.y === 0) {
        yPos = y * params.scale;
      } else {
        yPos = y * params.scale + params.y;
      }
      return `(xy ${xPos} ${yPos})`;
    };
    const points = chunks
      .map((p) => {
        return p.map(pos).join(" ");
      })
      // fill none/solid
      .map((p) => {
        return `(gr_poly
                (pts${p})
                (stroke (width 0) (type solid)) (fill none) (layer "B.Mask")
            )
            (gr_poly
                (pts${p})
                (stroke (width 0) (type solid)) (fill solid) (layer "B.Cu")
            )
            (gr_poly
                (pts${p})
                (stroke (width 0) (type solid)) (fill none) (layer "F.Mask")
            )
            (gr_poly
                (pts${p})
                (stroke (width 0) (type solid)) (fill none) (layer "F.Cu")
            )`;
      })
      .join("\n");
    return points;
  },
};