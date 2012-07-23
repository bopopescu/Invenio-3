body = '''<div class="mainContainerLayer">
    <div class="figurePlotsSelector" id="figuresSelector">
        <div id="figureMiniaturesSelector" class="figureMiniaturesPlaceholder">
        </div>
        <input type="button" value="Create new figure" id="btnNewPlot">
    </div>

    <div class="documentPageSelector" id="pagesSelectorLayer"></div>

    <div class="pageView" id="pageViewArea">
        <!--
        <div id="calculated0" style ="width: 2px; height : 2px; background-color: #0f0; position: absolute; z-index:1000"></div>
        <div id="calculated1" style ="width: 2px; height : 2px; background-color: #0f0; position: absolute; z-index:1000"></div>
        <div id="calculated2" style ="width: 2px; height : 2px; background-color: #0f0; position: absolute; z-index:1000"></div>
        <div id="calculated3" style ="width: 2px; height : 2px; background-color: #0f0; position: absolute; z-index:1000"></div>
        -->
    </div>

    <div class="figureControls" id="figureControlsLayer">
        <h2>Current figure:</h2>

        <div>
            Figure image:
            <div id="figurePreviewPalceholder" class="previewPlaceholder"></div>
            Figure coordinates: <p id="lblFigureBoundary"></p>
            <input type="button" id="btnSelectFigureContent" value="Select the boundary"/>
        </div>
        <div>
            <input type="button" id="btnSelectFigureCaption" value="Select caption" />
            <input type="button" id="btnExtractCaption" value="Extract caption text" /> <br/>
            Caption text:
            <textarea id="figureCaptionText" class="captionTextInput">TODO: Text should be automaticaly extracted from the selected caption and should be inputed into this field
            </textarea>
            Caption preview:
            <div id="captionPreviewPlaceholder" class="previewPlaceholder"></div>
            Caption coordinates:
            <p id="lblCaptionBoundary"></p>
        </div>
        <br>
        <div>
            <input type="button" value="Remove figure" id="btnRemoveFigure" />
        </div>
        <div>
            <input type="button" value="Save" id="btnSave" />
        </div>
        <div>
            <input type="button" value="Approve" id="btnApprove" />
        </div>
    </div>
    <div id="busLog"></div>

</div>

<br>
<div id="eventsBusLog" class="logLayer">
    <div style="display: table-row;">
        <div style="display: table-cell;"><b>Event name</b></div>
        <div style="display: table-cell;"><b>Event subject</b></div>
        <div style="display: table-cell;"><b>Event arguments</b></div>
    </div>
</div>
'''