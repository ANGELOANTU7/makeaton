
"use strict";

let CleanupLocalGrids = require('./CleanupLocalGrids.js')
let SetLabel = require('./SetLabel.js')
let GetMap = require('./GetMap.js')
let ResetPose = require('./ResetPose.js')
let GlobalBundleAdjustment = require('./GlobalBundleAdjustment.js')
let PublishMap = require('./PublishMap.js')
let GetMap2 = require('./GetMap2.js')
let GetNodeData = require('./GetNodeData.js')
let SetGoal = require('./SetGoal.js')
let GetNodesInRadius = require('./GetNodesInRadius.js')
let LoadDatabase = require('./LoadDatabase.js')
let RemoveLabel = require('./RemoveLabel.js')
let AddLink = require('./AddLink.js')
let GetPlan = require('./GetPlan.js')
let ListLabels = require('./ListLabels.js')
let DetectMoreLoopClosures = require('./DetectMoreLoopClosures.js')

module.exports = {
  CleanupLocalGrids: CleanupLocalGrids,
  SetLabel: SetLabel,
  GetMap: GetMap,
  ResetPose: ResetPose,
  GlobalBundleAdjustment: GlobalBundleAdjustment,
  PublishMap: PublishMap,
  GetMap2: GetMap2,
  GetNodeData: GetNodeData,
  SetGoal: SetGoal,
  GetNodesInRadius: GetNodesInRadius,
  LoadDatabase: LoadDatabase,
  RemoveLabel: RemoveLabel,
  AddLink: AddLink,
  GetPlan: GetPlan,
  ListLabels: ListLabels,
  DetectMoreLoopClosures: DetectMoreLoopClosures,
};
