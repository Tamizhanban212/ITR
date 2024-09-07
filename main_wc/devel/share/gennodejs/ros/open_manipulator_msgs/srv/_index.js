
"use strict";

let GetKinematicsPose = require('./GetKinematicsPose.js')
let SetKinematicsPose = require('./SetKinematicsPose.js')
let SetDrawingTrajectory = require('./SetDrawingTrajectory.js')
let SetActuatorState = require('./SetActuatorState.js')
let GetJointPosition = require('./GetJointPosition.js')
let SetJointPosition = require('./SetJointPosition.js')

module.exports = {
  GetKinematicsPose: GetKinematicsPose,
  SetKinematicsPose: SetKinematicsPose,
  SetDrawingTrajectory: SetDrawingTrajectory,
  SetActuatorState: SetActuatorState,
  GetJointPosition: GetJointPosition,
  SetJointPosition: SetJointPosition,
};
