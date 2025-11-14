#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 08/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------


class Saver:

    def audacity_label(ann, outfp):
        """
        Saves annotation as a text file.
        It can be opened in audacity for inspection.
    
        Paramters
        ---------
        ann: list[tuple[float, float, str]]
            - List of (start, end, label).
        outfp: str
            - Filepath to save the annotation.
        """
        
        from ._annotation import AnnotationSaver
        
        AnnotationSaver._audacity_label(ann, outfp)
        
    def ctm_label(ann, outfp, segment_id="utt1", channel=1):
        """
        Saves annotation in CTM format.
    
        Parameters
        ----------
        ann: list[tuple[float, float, str]]
            List of (start, end, label).
        outfp: str
            Filepath to save the annotation.
        segment_id: str
            Segment/utterance ID (default "utt1").
        channel: int
            Audio channel (default 1).
        """
        
        from ._annotation import AnnotationSaver
        AnnotationSaver._ctm_label(ann, outfp, segment_id, channel)
        
    def textgrid_label(ann, outfp, tier_name="labels"):
        """
        Saves annotation as a Praat TextGrid.
    
        Parameters
        ----------
        ann: list[tuple[float, float, str]]
            List of (start, end, label).
        outfp: str
            Filepath to save the annotation.
        tier_name: str
            Name of the TextGrid tier.
        """
        from ._annotation import AnnotationSaver
        AnnotationSaver._textgrid_label(ann, outfp, tier_name)
        
        