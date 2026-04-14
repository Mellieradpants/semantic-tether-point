import { LegislativeNode } from "@/data/legislativeData";

export interface SelectionDropReason {
  nodeId: string;
  reason:
    | "missing_id"
    | "missing_text"
    | "missing_type"
    | "empty_text"
    | "label_echo_container"
    | "duplicated_container_text";
}

export interface SelectionResult {
  selectedNodes: LegislativeNode[];
  selectionMetadata: {
    totalInputNodes: number;
    totalSelectedNodes: number;
    droppedNodeIds: string[];
    dropReasons: SelectionDropReason[];
  };
  errors: string[];
  canProceed: boolean;
}

function normalizeText(value: string): string {
  return value.trim().replace(/\s+/g, " ");
}

function isContainerWithDuplicatedText(
  node: LegislativeNode,
  allNodes: LegislativeNode[]
): boolean {
  const children = allNodes.filter((n) => n.parentId === node.id);
  if (children.length === 0) return false;

  const childTextCombined = children
    .map((c) => normalizeText(c.text))
    .join(" ");

  const nodeTextNormalized = normalizeText(node.text);
  const nodeLabelNormalized = normalizeText(node.label);

  if (nodeTextNormalized === childTextCombined) return true;

  if (nodeTextNormalized === nodeLabelNormalized) return true;

  if (children.length > 1) {
    let remainder = nodeTextNormalized;

    for (const child of children) {
      const childNorm = normalizeText(child.text);

      if (childNorm && remainder.includes(childNorm)) {
        remainder = remainder.replace(childNorm, "");
      } else {
        return false;
      }
    }

    if (remainder.replace(/[\s.,;:—–\-]/g, "").length === 0) {
      return true;
    }
  }

  return false;
}

export function selectLegislativeNodes(
  nodes: LegislativeNode[]
): SelectionResult {
  const selectedNodes: LegislativeNode[] = [];
  const dropReasons: SelectionDropReason[] = [];
  const errors: string[] = [];

  for (const node of nodes) {
    if (!node.id) {
      dropReasons.push({ nodeId: "", reason: "missing_id" });
      continue;
    }

    if (typeof node.text !== "string") {
      dropReasons.push({ nodeId: node.id, reason: "missing_text" });
      continue;
    }

    if (!node.type) {
      dropReasons.push({ nodeId: node.id, reason: "missing_type" });
      continue;
    }

    if (normalizeText(node.text).length === 0) {
      dropReasons.push({ nodeId: node.id, reason: "empty_text" });
      continue;
    }

    const children = nodes.filter((n) => n.parentId === node.id);
    const hasChildren = children.length > 0;

    if (hasChildren) {
      if (normalizeText(node.text) === normalizeText(node.label)) {
        dropReasons.push({
          nodeId: node.id,
          reason: "label_echo_container",
        });
        continue;
      }

      if (isContainerWithDuplicatedText(node, nodes)) {
        dropReasons.push({
          nodeId: node.id,
          reason: "duplicated_container_text",
        });
        continue;
      }
    }

    selectedNodes.push(node);
  }

  return {
    selectedNodes,
    selectionMetadata: {
      totalInputNodes: nodes.length,
      totalSelectedNodes: selectedNodes.length,
      droppedNodeIds: dropReasons.map((item) => item.nodeId),
      dropReasons,
    },
    errors,
    canProceed: selectedNodes.length > 0,
  };
}
