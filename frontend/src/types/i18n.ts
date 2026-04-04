export type TranslationValue =
  | string
  | number
  | boolean
  | null
  | TranslationNode
  | TranslationValue[];

export interface TranslationNode {
  [key: string]: TranslationValue;
}
