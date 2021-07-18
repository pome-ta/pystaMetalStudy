//
//  ViewController.swift
//  metal01
//
//  Created by pome-ta on 2021/07/16.
//

import UIKit
import Metal
import MetalKit

class ViewController: UIViewController {
    var mtkView: MTKView!
    var renderer: Renderer!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        guard let mtkViewTemp = self.view as? MTKView else {
            print("View")
            return
        }
        mtkView = mtkViewTemp

        guard let defaultDevice = MTLCreateSystemDefaultDevice() else {
            print("Divice")
            return
        }
        print("My GPU is: \(defaultDevice)")
        mtkView.device = defaultDevice

        guard let tempRenderer = Renderer(mtkView: mtkView) else {
            print("init")
            return
        }
        renderer = tempRenderer
        mtkView.delegate = renderer
    }


}

