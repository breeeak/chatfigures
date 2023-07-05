import {StateEnum} from "@/core/plugins/DrawEditor/overlay";
// 判断两个矩形是否相交 包含在内部的情况 https://www.yiiven.cn/rect-is-intersection.html
export const isIntersection = (rectA, rectB) => {
    //rect = [[x1,y1],[x2,y2]] x1 < x2, y1 < y2
    const lftp = [Math.max(rectA[0][0], rectB[0][0]), Math.max(rectA[0][1], rectB[0][1])],
        rgbt = [Math.min(rectA[1][0], rectB[1][0]), Math.min(rectA[1][1], rectB[1][1])];
    if (lftp[0] < rgbt[0] && lftp[1] < rgbt[1]) {
        return true;
    }
    return false;
}
// 计算两个矩形相交的面积
export const getIntersectionArea = (rectA, rectB) => {
    //rect = [[x1,y1],[x2,y2]] x1 < x2, y1 < y2
    rectA = [[Math.min(rectA[0][0], rectA[1][0]), Math.min(rectA[0][1], rectA[1][1])],[Math.max(rectA[0][0], rectA[1][0]), Math.max(rectA[0][1], rectA[1][1])]];
    rectB = [[Math.min(rectB[0][0], rectB[1][0]), Math.min(rectB[0][1], rectB[1][1])],[Math.max(rectB[0][0], rectB[1][0]), Math.max(rectB[0][1], rectB[1][1])]];
    const lftp = [Math.max(rectA[0][0], rectB[0][0]), Math.max(rectA[0][1], rectB[0][1])],
        rgbt = [Math.min(rectA[1][0], rectB[1][0]), Math.min(rectA[1][1], rectB[1][1])];
    if (lftp[0] < rgbt[0] && lftp[1] < rgbt[1]) {
        return (rgbt[0] - lftp[0]) * (rgbt[1] - lftp[1]);
    }
    return 0;
}


// 生成UUID
export function getUUID() {
    return 'xxxxxxxxxxxxxxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = (Math.random() * 16) | 0,
            v = c == 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}


// 生成随机颜色
export const getRandomColor = function (i) {
    const colorPalate = ["#D6D5B7", "#D1BA74", "#E6CEAC", "#ECAD9E", "#BEE7E9",
        "#554348", "#5fad41", "#2D936C", "#3A0842", "#391463",
        "#19CAAD", "#8CC7B5", "#A0EEE1", "#BEEDC7", "#BFAE48",
        "#747578",];
    if (i >= colorPalate.length || i<0) {
        return '#' + ('00000' + (Math.random() * 0x1000000 << 0).toString(16)).substr(-6);
    } else {
        return colorPalate[i];
    }
    //
}
export const measureRect = (width, height, ppm = 0) => {        // ppm为0表示未知 使用px即可
    width = Math.abs(Math.round(width))
    height = Math.abs(Math.round(height))
    const lineLength = Math.round((width + height) * 2);
    const area = Math.round(width * height);
    const {number: actLineLength, unit: actLineUnit} = px2actLength(
        lineLength,
        ppm
    );
    const {number: actWidth, unit: actWidthUnit} = px2actLength(
        width,
        ppm
    );
    const {number: actHeight, unit: actHeightUnit} = px2actLength(
        height,
        ppm
    );
    const actArea = parseFloat((actWidth * actHeight).toFixed(2));
    const actAreaUnit = actLineUnit;
    const results = {
        ppm,

        width,
        actWidth,
        actWidthUnit,

        height,
        actHeight,
        actHeightUnit,

        lineLength,
        actLineLength,
        actLineUnit,

        area,
        actArea,
        actAreaUnit,
    };
    return results;
}

export const measureCircle = (radius, ppm = 0) => {        // ppm为0表示未知 使用px即可
    radius = Math.abs(radius)
    const lineLength = Math.round(2 * Math.PI * radius);
    const area = Math.round(Math.PI * radius * radius);
    const {number: actLineLength, unit: actLineUnit} = px2actLength(
        lineLength,
        ppm
    );
    const {number: actRadius, unit: actRadiusUnit} = px2actLength(
        radius,
        ppm
    );
    radius = Math.round(radius);
    const actArea = parseFloat((2 * Math.PI * actRadius).toFixed(2));
    const actAreaUnit = actLineUnit;
    const results = {
        ppm,

        radius,
        actRadius,
        actRadiusUnit,

        lineLength,
        actLineLength,
        actLineUnit,

        area,
        actArea,
        actAreaUnit,
    };
    return results;
}

export const measureLine = (point, lastPoint, ppm = 0) => {        // ppm为0表示未知 使用px即可
    const lineLength = Math.round(
        Math.sqrt(
            (lastPoint.x - point.x) * (lastPoint.x - point.x) +
            (lastPoint.y - point.y) * (lastPoint.y - point.y)
        )
    );
    const {number: actLineLength, unit: actLineUnit} = px2actLength(
        lineLength,
        ppm
    );
    const results = {
        ppm,
        lineLength,
        actLineLength,
        actLineUnit,
    };
    return results;
}
export const measurePoly = (points, ppm = 0) => {        // ppm为0表示未知 使用px即可
    const {area, actArea, lineLength, actLineLength, unit} = polygonArea(points, ppm);

    const results = {
        ppm,
        lineLength,
        actLineLength,
        actLineUnit: unit,

        area,
        actArea,
        actAreaUnit: unit,
    };
    return results;
}

// 计算多边形的面积
const polygonArea = (points, ppm) => {
    let i, j;
    let area = 0;
    let lineLength = 0;
    for (i = 0; i < points.length; i++) {
        j = (i + 1) % points.length;
        area += points[i].x * points[j].y;
        area -= points[i].y * points[j].x;
        if (i + 1 < points.length) {
            let cLength =
                Math.sqrt(
                    (points[i + 1].x - points[i].x) * (points[i + 1].x - points[i].x) +
                    (points[i + 1].y - points[i].y) * (points[i + 1].y - points[i].y)
                );
            cLength = Math.max(cLength, 0);
            lineLength = lineLength + cLength;
        }
    }
    area /= 2;
    const {number: actLineLength, unit: actLineUnit} = px2actLength(
        lineLength,
        ppm
    );
    const {number: actArea, unit: actAreaUnit} = px2actLength(
        area,
        ppm * ppm
    );  //TODO check 这么算面积对不对
    return {
        area: Math.round(Math.abs(area)),
        actArea: actArea,
        lineLength: Math.round(lineLength),
        actLineLength: actLineLength,
        unit: actLineUnit,
    };
};

export const showTextInfo = (results, type, options) => {// 如果options 为false就全部显示  如果想不显示text的应该直接不绘制
    if (!options) {
        options = {
            basics: true,
            perimeters: true,
            areas: true,
            actual: true,
            unit: true
        }
    }

    if (results.ppm == 0) {     //没有对应的实际比例 不显示
        options.actual = false
    }
    const showTexts = ["", "", ""]
    if (options.basics) {
        if (type == StateEnum.RECT) {
            if (options.actual) {
                showTexts[0] = `Width:${results.width}px ${results.actWidth}${results.actWidthUnit}\nHeight:${results.height}px ${results.actHeight}${results.actHeightUnit}`
            } else {
                showTexts[0] = `Width:${results.width}px\nHeight:${results.height}px`
            }
        } else if (type == StateEnum.CIRCLE) {
            if (options.actual) {
                showTexts[0] = `Radius:${results.radius}px ${results.actRadius}${results.actRadiusUnit}`
            } else {
                showTexts[0] = `Radius:${results.radius}px`
            }
        }
    }
    if (options.perimeters) {
        if (options.actual) {
            showTexts[1] = `Perimeter:${results.lineLength}px ${results.actLineLength}${results.actLineUnit}`
        } else {
            showTexts[1] = `Perimeter:${results.lineLength}px`
        }
        if (type == StateEnum.LINE) {
            showTexts[1] = showTexts[1].replace("Perimeter:", "")
        }
    }
    if (options.areas) {
        if (type != StateEnum.LINE) {
            if (options.actual) {
                showTexts[2] = `Area:${results.area}px² ${results.actArea}${results.actAreaUnit}²`
            } else {
                showTexts[2] = `Area:${results.area}px²`
            }
        }
    }
    const outText = showTexts.join("\n")
    if (options.unit) {
        return outText
    } else {
        return outText.replace("px", "").replace("²", "")
    }
}


// px2actlength
const px2actLength = (px, ppi) => {
    if (ppi && ppi != 0) {
        let actLength = px / ppi;
        if (actLength >= 1000) {
            actLength = parseFloat(Number(actLength / 1000).toFixed(2));
            return {number: actLength, unit: "km"};
        } else if (actLength >= 1 && actLength <= 1000) {
            actLength = parseFloat(Number(actLength).toFixed(2));
            return {number: actLength, unit: "m"};
        } else if (actLength >= 1e-3 && actLength <= 1) {
            actLength = parseFloat(Number(actLength / 1e-3).toFixed(2));
            return {number: actLength, unit: "mm"};
        } else if (actLength >= 1e-6 && actLength <= 1e-3) {
            actLength = parseFloat(Number(actLength / 1e-6).toFixed(2));
            return {number: actLength, unit: "μm"};
        } else if (actLength >= 1e-9 && actLength <= 1e-6) {
            actLength = parseFloat(Number(actLength / 1e-9).toFixed(2));
            return {number: actLength, unit: "nm"};
        } else {
            return {number: actLength, unit: "m"};
        }
    } else {
        return {number: px, unit: "px"};
    }
};

