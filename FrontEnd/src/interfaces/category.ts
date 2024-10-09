import Source from "./source.ts";

export default interface Category {
    id: number,
    name: string,
    risk: number,
    sources: Source[],
    weight: number
}